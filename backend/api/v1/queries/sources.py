from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundException
from database import get_db_session
from repositories.source_repository import SourceRepository
from schemas import (
    Source, 
    SourceDetail, 
    APIResponse, 
    PaginatedResponse,
    SourceSearchParams,
    CoordinateSearchParams
)

# Create router for source queries
router = APIRouter(prefix="/sources", tags=["Sources"])

# Create repository instance
source_repo = SourceRepository()


@router.get("/", response_model=PaginatedResponse[Source])
async def get_sources(
    params: SourceSearchParams = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a paginated list of sources.
    
    Args:
        params: Pagination and search parameters
        db: Database session
        
    Returns:
        Paginated list of sources
    """
    # Get total count for pagination
    total = await source_repo.get_total_count(db)
    
    # Get sources with pagination
    sources = await source_repo.get_multi(db, skip=params.skip, limit=params.limit)
    
    # Create response with pagination metadata
    return PaginatedResponse(
        items=sources,
        **params.to_page_response(total)
    )


@router.get("/coordinates", response_model=PaginatedResponse[Source])
async def search_by_coordinates(
    params: CoordinateSearchParams = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Search sources by coordinates within a radius.
    
    Args:
        params: Coordinate search parameters
        db: Database session
        
    Returns:
        Paginated list of sources within the specified radius
    """
    # Search sources by coordinates
    sources = await source_repo.search_by_coordinates(
        db, 
        ra=params.ra, 
        declination=params.declination, 
        radius=params.radius,
        skip=params.skip,
        limit=params.limit
    )
    
    # For pagination, we'd need the total count within radius
    # This is approximate as we're not querying for total
    total = len(sources) if params.skip == 0 and len(sources) < params.limit else params.limit + 1
    
    return PaginatedResponse(
        items=sources,
        **params.to_page_response(total)
    )


@router.get("/{agn_id}", response_model=APIResponse)
async def get_source_by_id(
    agn_id: int = Path(..., description="AGN ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a source by ID with all related data.
    
    Args:
        agn_id: AGN ID
        db: Database session
        
    Returns:
        Source with all related data
    
    Raises:
        NotFoundException: If source not found
    """
    # Get source with related data
    source_data = await source_repo.get_by_id_with_related(db, agn_id)
    if not source_data:
        raise NotFoundException(f"Source with ID {agn_id} not found")
    
    return APIResponse(
        success=True,
        message=f"Source with ID {agn_id} retrieved successfully",
        data=source_data
    ) 