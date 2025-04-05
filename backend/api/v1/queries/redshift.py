from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundException
from database import get_db_session
from repositories.redshift_repository import RedshiftRepository
from schemas import (
    Redshift,
    APIResponse,
    PaginatedResponse,
    RedshiftSearchParams,
    PaginationParams
)

# Create router for redshift queries
router = APIRouter(prefix="/redshift", tags=["Redshift"])

# Create repository instance
redshift_repo = RedshiftRepository()


@router.get("/", response_model=PaginatedResponse[Redshift])
async def get_redshifts(
    params: RedshiftSearchParams = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a paginated list of redshift measurements with optional filters.
    
    Args:
        params: Search and pagination parameters
        db: Database session
        
    Returns:
        Paginated list of redshift measurements
    """
    # Build query based on parameters
    query = None
    
    # If specific filters are provided, use specialized repository methods
    if params.redshift_type:
        redshifts = await redshift_repo.get_by_redshift_type(
            db, params.redshift_type, params.skip, params.limit
        )
        # For simplicity, we'll approximate total count
        total = len(redshifts) if len(redshifts) < params.limit else params.limit + params.skip
    elif params.min_z is not None or params.max_z is not None:
        redshifts = await redshift_repo.get_by_redshift_range(
            db, params.min_z, params.max_z, params.skip, params.limit
        )
        # For simplicity, we'll approximate total count
        total = len(redshifts) if len(redshifts) < params.limit else params.limit + params.skip
    elif params.agn_id:
        redshifts = await redshift_repo.get_by_agn_id(db, params.agn_id)
        total = len(redshifts)
        # Apply pagination manually since we got all records
        redshifts = redshifts[params.skip:params.skip + params.limit] if redshifts else []
    else:
        # No specific filters, get all with pagination
        redshifts = await redshift_repo.get_multi(db, skip=params.skip, limit=params.limit)
        # Get approximate total count
        stats = await redshift_repo.get_statistics(db)
        total = stats["count"]
    
    # Create response with pagination metadata
    return PaginatedResponse(
        items=redshifts,
        **params.to_page_response(total)
    )


@router.get("/source/{agn_id}", response_model=APIResponse)
async def get_redshifts_by_source(
    agn_id: int = Path(..., description="AGN source ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get all redshift measurements for a specific source.
    
    Args:
        agn_id: AGN source ID
        db: Database session
        
    Returns:
        All redshift measurements for the source
    """
    redshifts = await redshift_repo.get_by_agn_id(db, agn_id)
    
    if not redshifts:
        return APIResponse(
            success=True,
            message=f"No redshift measurements found for source with ID {agn_id}",
            data=[]
        )
    
    return APIResponse(
        success=True,
        message=f"Retrieved {len(redshifts)} redshift measurements for source with ID {agn_id}",
        data=redshifts
    )


@router.get("/type/{redshift_type}", response_model=PaginatedResponse[Redshift])
async def get_redshifts_by_type(
    redshift_type: str = Path(..., description="Type of redshift measurement"),
    params: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get redshift measurements of a specific type.
    
    Args:
        redshift_type: Type of redshift measurement
        params: Pagination parameters
        db: Database session
        
    Returns:
        Paginated list of redshift measurements of the specified type
    """
    redshifts = await redshift_repo.get_by_redshift_type(
        db, redshift_type, params.skip, params.limit
    )
    
    # For simplicity, we'll approximate total count
    total = len(redshifts) if len(redshifts) < params.limit else params.limit + params.skip
    
    return PaginatedResponse(
        items=redshifts,
        **params.to_page_response(total)
    )


@router.get("/range", response_model=PaginatedResponse[Redshift])
async def get_redshifts_by_range(
    min_z: Optional[float] = Query(None, ge=0.0, description="Minimum redshift value"),
    max_z: Optional[float] = Query(None, ge=0.0, description="Maximum redshift value"),
    params: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get redshift measurements within a redshift range.
    
    Args:
        min_z: Minimum redshift value (inclusive)
        max_z: Maximum redshift value (inclusive)
        params: Pagination parameters
        db: Database session
        
    Returns:
        Paginated list of redshift measurements within the specified range
    """
    if min_z is None and max_z is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one of min_z or max_z must be provided"
        )
    
    redshifts = await redshift_repo.get_by_redshift_range(
        db, min_z, max_z, params.skip, params.limit
    )
    
    # For simplicity, we'll approximate total count
    total = len(redshifts) if len(redshifts) < params.limit else params.limit + params.skip
    
    return PaginatedResponse(
        items=redshifts,
        **params.to_page_response(total)
    )


@router.get("/statistics", response_model=APIResponse)
async def get_redshift_statistics(
    redshift_type: Optional[str] = Query(None, description="Optional redshift type to filter by"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get statistics about redshift measurements.
    
    Args:
        redshift_type: Optional redshift type to filter by
        db: Database session
        
    Returns:
        Statistics about redshift measurements (count, avg_redshift, etc.)
    """
    stats = await redshift_repo.get_statistics(db, redshift_type)
    
    return APIResponse(
        success=True,
        message="Retrieved redshift statistics",
        data=stats
    )


@router.get("/source/{agn_id}/average", response_model=APIResponse)
async def get_average_redshift_for_source(
    agn_id: int = Path(..., description="AGN source ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get the average redshift for a specific source.
    
    Args:
        agn_id: AGN source ID
        db: Database session
        
    Returns:
        Average redshift value for the source
    """
    avg_z = await redshift_repo.get_average_redshift(db, agn_id)
    
    if avg_z is None:
        return APIResponse(
            success=True,
            message=f"No redshift measurements found for source with ID {agn_id}",
            data={"average_redshift": None}
        )
    
    return APIResponse(
        success=True,
        message=f"Retrieved average redshift for source with ID {agn_id}",
        data={"average_redshift": avg_z}
    )


@router.get("/source/{agn_id}/types", response_model=APIResponse)
async def get_redshift_types_for_source(
    agn_id: int = Path(..., description="AGN source ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get all unique redshift types for a specific source.
    
    Args:
        agn_id: AGN source ID
        db: Database session
        
    Returns:
        List of unique redshift types for the source
    """
    types = await redshift_repo.get_redshift_types_for_source(db, agn_id)
    
    if not types:
        return APIResponse(
            success=True,
            message=f"No redshift measurements found for source with ID {agn_id}",
            data={"redshift_types": []}
        )
    
    return APIResponse(
        success=True,
        message=f"Retrieved {len(types)} redshift types for source with ID {agn_id}",
        data={"redshift_types": types}
    )


@router.get("/{redshift_id}", response_model=APIResponse)
async def get_redshift_by_id(
    redshift_id: int = Path(..., description="Redshift measurement ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a redshift measurement by ID.
    
    Args:
        redshift_id: Redshift measurement ID
        db: Database session
        
    Returns:
        Redshift measurement with the specified ID
        
    Raises:
        NotFoundException: If redshift measurement not found
    """
    redshift = await redshift_repo.get_by_redshift_id(db, redshift_id)
    
    if not redshift:
        raise NotFoundException(f"Redshift measurement with ID {redshift_id} not found")
    
    return APIResponse(
        success=True,
        message=f"Retrieved redshift measurement with ID {redshift_id}",
        data=redshift
    ) 