from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundException
from database import get_db_session
from repositories.photometry_repository import PhotometryRepository
from schemas import (
    Photometry, 
    APIResponse, 
    PaginatedResponse,
    PhotometrySearchParams,
    BandSearchParams,
    FilterSearchParams,
    MagnitudeRangeParams,
    PaginationParams
)

# Create router for photometry queries
router = APIRouter(prefix="/photometry", tags=["Photometry"])

# Create repository instance
photometry_repo = PhotometryRepository()


@router.get("/", response_model=PaginatedResponse[Photometry])
async def get_photometry(
    params: PhotometrySearchParams = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a paginated list of photometry measurements with optional filters.
    
    Args:
        params: Search and pagination parameters
        db: Database session
        
    Returns:
        Paginated list of photometry measurements
    """
    # Build query based on parameters
    query = None
    
    # If specific filters are provided, use specialized repository methods
    if params.band_label:
        photometry = await photometry_repo.get_by_band(
            db, params.band_label, params.skip, params.limit
        )
        # For simplicity, we'll approximate total count
        total = len(photometry) if len(photometry) < params.limit else params.limit + params.skip
    elif params.filter_name:
        photometry = await photometry_repo.get_by_filter(
            db, params.filter_name, params.skip, params.limit
        )
        # For simplicity, we'll approximate total count
        total = len(photometry) if len(photometry) < params.limit else params.limit + params.skip
    elif params.min_mag is not None or params.max_mag is not None:
        photometry = await photometry_repo.get_by_magnitude_range(
            db, params.min_mag, params.max_mag, params.skip, params.limit
        )
        # For simplicity, we'll approximate total count
        total = len(photometry) if len(photometry) < params.limit else params.limit + params.skip
    elif params.agn_id:
        photometry = await photometry_repo.get_by_agn_id(db, params.agn_id)
        total = len(photometry)
        # Apply pagination manually since we got all records
        photometry = photometry[params.skip:params.skip + params.limit]
    else:
        # No specific filters, get all with pagination
        photometry = await photometry_repo.get_multi(db, skip=params.skip, limit=params.limit)
        # Get approximate total count
        stats = await photometry_repo.get_statistics(db)
        total = stats["count"]
    
    # Create response with pagination metadata
    return PaginatedResponse(
        items=photometry,
        **params.to_page_response(total)
    )


@router.get("/source/{agn_id}", response_model=APIResponse)
async def get_photometry_by_source(
    agn_id: int = Path(..., description="AGN source ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get all photometry measurements for a specific source.
    
    Args:
        agn_id: AGN source ID
        db: Database session
        
    Returns:
        All photometry measurements for the source
    """
    photometry = await photometry_repo.get_by_agn_id(db, agn_id)
    
    if not photometry:
        return APIResponse(
            success=True,
            message=f"No photometry found for source with ID {agn_id}",
            data=[]
        )
    
    return APIResponse(
        success=True,
        message=f"Retrieved {len(photometry)} photometry measurements for source with ID {agn_id}",
        data=photometry
    )


@router.get("/band/{band_label}", response_model=PaginatedResponse[Photometry])
async def get_photometry_by_band(
    band_label: str = Path(..., description="Photometric band label"),
    params: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get photometry measurements for a specific band.
    
    Args:
        band_label: Photometric band label (e.g., 'U', 'B', 'V')
        params: Pagination parameters
        db: Database session
        
    Returns:
        Paginated list of photometry measurements for the specified band
    """
    photometry = await photometry_repo.get_by_band(
        db, band_label, params.skip, params.limit
    )
    
    # For simplicity, we'll approximate total count
    total = len(photometry) if len(photometry) < params.limit else params.limit + params.skip
    
    return PaginatedResponse(
        items=photometry,
        **params.to_page_response(total)
    )


@router.get("/filter/{filter_name}", response_model=PaginatedResponse[Photometry])
async def get_photometry_by_filter(
    filter_name: str = Path(..., description="Filter name"),
    params: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get photometry measurements for a specific filter.
    
    Args:
        filter_name: Filter name (e.g., 'SDSS u', '2MASS J')
        params: Pagination parameters
        db: Database session
        
    Returns:
        Paginated list of photometry measurements for the specified filter
    """
    photometry = await photometry_repo.get_by_filter(
        db, filter_name, params.skip, params.limit
    )
    
    # For simplicity, we'll approximate total count
    total = len(photometry) if len(photometry) < params.limit else params.limit + params.skip
    
    return PaginatedResponse(
        items=photometry,
        **params.to_page_response(total)
    )


@router.get("/magnitude-range", response_model=PaginatedResponse[Photometry])
async def get_photometry_by_magnitude_range(
    params: MagnitudeRangeParams = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get photometry measurements within a magnitude range.
    
    Args:
        params: Magnitude range and pagination parameters
        db: Database session
        
    Returns:
        Paginated list of photometry measurements within the specified magnitude range
    """
    if params.min_mag is None and params.max_mag is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one of min_mag or max_mag must be provided"
        )
    
    photometry = await photometry_repo.get_by_magnitude_range(
        db, params.min_mag, params.max_mag, params.skip, params.limit
    )
    
    # For simplicity, we'll approximate total count
    total = len(photometry) if len(photometry) < params.limit else params.limit + params.skip
    
    return PaginatedResponse(
        items=photometry,
        **params.to_page_response(total)
    )


@router.get("/statistics", response_model=APIResponse)
async def get_photometry_statistics(
    agn_id: Optional[int] = Query(None, description="Optional AGN source ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get statistics for photometry data.
    
    Args:
        agn_id: Optional AGN source ID to limit statistics to a specific source
        db: Database session
        
    Returns:
        Statistics for photometry data
    """
    stats = await photometry_repo.get_statistics(db, agn_id)
    
    source_str = f" for source with ID {agn_id}" if agn_id else ""
    return APIResponse(
        success=True,
        message=f"Retrieved photometry statistics{source_str}",
        data=stats
    )


@router.get("/{phot_id}", response_model=APIResponse)
async def get_photometry_by_id(
    phot_id: int = Path(..., description="Photometry measurement ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a specific photometry measurement by ID.
    
    Args:
        phot_id: Photometry measurement ID
        db: Database session
        
    Returns:
        Photometry measurement
        
    Raises:
        NotFoundException: If photometry measurement not found
    """
    photometry = await photometry_repo.get_by_phot_id(db, phot_id)
    
    if not photometry:
        raise NotFoundException(f"Photometry measurement with ID {phot_id} not found")
    
    return APIResponse(
        success=True,
        message=f"Retrieved photometry measurement with ID {phot_id}",
        data=photometry
    ) 