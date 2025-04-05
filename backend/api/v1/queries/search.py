from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Body, Query, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
import io

from database import get_db_session
from schemas import (
    PaginatedResponse,
    PaginationParams,
    APIResponse,
    ExportOptions,
    ExportFormat
)
from repositories.search_repository import SearchRepository
from services.export_service import ExportService

# Create router for search queries
router = APIRouter(prefix="/search", tags=["Search"])

# Create repository instance
search_repo = SearchRepository()
# Create export service instance
export_service = ExportService()


@router.post("/", response_model=PaginatedResponse)
async def search(
    query: Dict[str, Any] = Body(..., description="Search query from QueryBuilder"),
    params: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Execute a complex search query and return paginated results.
    
    This endpoint accepts a query object from the frontend QueryBuilder
    and converts it to appropriate SQL queries for searching the database.
    The query format follows react-querybuilder structure with a combinator
    ('and'/'or') and a list of rules that define the search conditions.
    
    Example query structure:
    ```json
    {
      "combinator": "and",
      "rules": [
        {"field": "ra", "operator": "<=", "value": "10"},
        {"field": "declination", "operator": ">", "value": "0"}
      ]
    }
    ```
    
    Args:
        query: The query object from the frontend QueryBuilder
        params: Pagination parameters (skip, limit, sort_field, sort_direction)
        db: Database session
        
    Returns:
        Paginated search results with metadata (total, page, etc.)
    """
    logger.info(f"Executing search query: {query}")
    
    try:
        # Execute search
        results, total = await search_repo.execute_query(
            db, 
            query, 
            skip=params.skip, 
            limit=params.limit,
            sort_field=params.sort_field,
            sort_direction=params.sort_direction
        )
        
        # Create response with pagination metadata
        return PaginatedResponse(
            items=results,
            **params.to_page_response(total)
        )
    except Exception as e:
        logger.error(f"Search query failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid search query: {str(e)}"
        )


@router.post("/export")
async def export_search_results(
    query: Dict[str, Any] = Body(..., description="Search query from QueryBuilder"),
    export_options: ExportOptions = Body(..., description="Export options"),
    sort_field: Optional[str] = Query(None, description="Field to sort by"),
    sort_direction: Optional[str] = Query("asc", description="Sort direction (asc or desc)"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Export search results in the specified format.
    
    This endpoint allows researchers to export search results to various formats
    for further analysis in external tools. The export process supports field
    selection, metadata inclusion, and data format options.
    
    Supported export formats:
    - CSV: Standard comma-separated values for general use
    - VOTable: XML format specifically for astronomical data that follows
      the Virtual Observatory standard for interoperability
    
    Args:
        query: The query object from the frontend QueryBuilder
        export_options: Options specifying:
            - format: Export format (CSV, VOTable)
            - selected_fields: List of fields to include in export
            - include_metadata: Whether to include metadata like units and descriptions
        sort_field: Field to sort results by
        sort_direction: Direction to sort (asc or desc)
        db: Database session
        
    Returns:
        Streaming response with the exported data and appropriate headers
        for browser download
    """
    logger.info(f"Exporting search results. Format: {export_options.format}, Query: {query}")
    
    try:
        # Execute search without pagination to get all matching results
        results, total = await search_repo.execute_query(
            db, 
            query,
            skip=0,
            limit=10000,  # Reasonable limit to prevent memory issues
            sort_field=sort_field,
            sort_direction=sort_direction
        )
        
        logger.info(f"Found {total} results to export")
        
        # Export based on requested format
        if export_options.format == ExportFormat.CSV:
            content = await export_service.export_to_csv(
                results,
                selected_fields=export_options.selected_fields,
                include_metadata=export_options.include_metadata
            )
            media_type = "text/csv"
            filename = "agn_db_export.csv"
        elif export_options.format == ExportFormat.VOTABLE:
            content = await export_service.export_to_votable(
                results,
                selected_fields=export_options.selected_fields,
                include_metadata=export_options.include_metadata
            )
            media_type = "application/xml"
            filename = "agn_db_export.xml"
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported export format: {export_options.format}"
            )
            
        # Create response with appropriate headers for download
        return StreamingResponse(
            io.StringIO(content),
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": media_type  # Set explicit Content-Type without charset
            }
        )
            
    except HTTPException as http_exc:
        # Re-raise HTTPExceptions with their original status code
        logger.error(f"Export failed with status {http_exc.status_code}: {http_exc.detail}")
        raise
    except Exception as e:
        # Log the general exception and wrap it in a 500 error
        logger.error(f"Export failed with unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Export failed: {str(e)}"
        )


@router.get("/available-fields")
async def get_available_fields(
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a list of all available fields for export and filtering.
    
    This endpoint helps the frontend dynamically generate field selection options
    for the export feature and search interface. Fields are categorized by their
    respective domain areas (source, photometry, etc.) to improve usability.
    
    The endpoint retrieves a sample of data to determine all possible fields,
    making it adaptable as the schema evolves.
    
    Args:
        db: Database session
        
    Returns:
        JSON object with:
        - categories: Dictionary of field names grouped by category
        - all_fields: Flat list of all available field names
    """
    try:
        # Get sample data to determine available fields
        sample_query = {}  # Empty query to get a small sample
        results, _ = await search_repo.execute_query(db, sample_query, limit=10)
        
        # Collect all unique fields
        all_fields = set()
        for item in results:
            all_fields.update(item.keys())
            
        # Get fields with categories
        categorized_fields = {
            "source": [field for field in all_fields if field in ["agn_id", "ra", "declination"]],
            "photometry": [field for field in all_fields if field in ["band_label", "filter_name", "mag_value", "mag_error", "extinction"]],
            "redshift": [field for field in all_fields if field in ["redshift_type", "z_value", "z_error"]],
            "classification": [field for field in all_fields if field in ["spec_class", "gen_class", "xray_class", "best_class", "image_class", "sed_class"]],
            "other": [field for field in all_fields if field not in 
                        ["agn_id", "ra", "declination"] + 
                        ["band_label", "filter_name", "mag_value", "mag_error", "extinction"] + 
                        ["redshift_type", "z_value", "z_error"] + 
                        ["spec_class", "gen_class", "xray_class", "best_class", "image_class", "sed_class"]]
        }
        
        # Return categorized fields
        return {
            "categories": categorized_fields,
            "all_fields": sorted(list(all_fields))
        }
        
    except HTTPException as http_exc:
        # Re-raise HTTPExceptions with their original status code
        logger.error(f"Failed to get available fields with status {http_exc.status_code}: {http_exc.detail}")
        raise
    except Exception as e:
        # Log the general exception and wrap it in a 500 error
        logger.error(f"Failed to get available fields with unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get available fields: {str(e)}"
        ) 