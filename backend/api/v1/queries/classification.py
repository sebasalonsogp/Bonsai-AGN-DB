from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundException
from database import get_db_session
from repositories.classification_repository import ClassificationRepository
from schemas import (
    Classification,
    APIResponse,
    PaginatedResponse,
    ClassificationSearchParams,
    PaginationParams
)

# Create router for classification queries
router = APIRouter(prefix="/classification", tags=["Classification"])

# Create repository instance
classification_repo = ClassificationRepository()


@router.get("/", response_model=PaginatedResponse[Classification])
async def get_classifications(
    params: ClassificationSearchParams = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a paginated list of classifications with optional filters.
    
    Args:
        params: Search and pagination parameters
        db: Database session
        
    Returns:
        Paginated list of classifications
    """
    # Build query based on parameters
    query = None
    
    # If specific filters are provided, use specialized repository methods
    if params.spec_class:
        classifications = await classification_repo.get_by_spec_class(
            db, params.spec_class, params.skip, params.limit
        )
        # For simplicity, we'll approximate total count
        total = len(classifications) if len(classifications) < params.limit else params.limit + params.skip
    elif params.gen_class:
        classifications = await classification_repo.get_by_gen_class(
            db, params.gen_class, params.skip, params.limit
        )
        # For simplicity, we'll approximate total count
        total = len(classifications) if len(classifications) < params.limit else params.limit + params.skip
    elif params.best_class:
        classifications = await classification_repo.get_by_best_class(
            db, params.best_class, params.skip, params.limit
        )
        # For simplicity, we'll approximate total count
        total = len(classifications) if len(classifications) < params.limit else params.limit + params.skip
    elif params.agn_id:
        classification = await classification_repo.get_by_agn_id(db, params.agn_id)
        if classification:
            classifications = [classification]
            total = 1
        else:
            classifications = []
            total = 0
    else:
        # No specific filters, get all with pagination
        classifications = await classification_repo.get_multi(db, skip=params.skip, limit=params.limit)
        # Get approximate total count by counting classifications with multiple types
        query_result = await classification_repo.get_classifications_with_multiple_types(
            db, skip=0, limit=1
        )
        # This is an approximation; in a real system, we'd have a better way to count total records
        total = len(query_result) + params.skip + params.limit
    
    # Create response with pagination metadata
    return PaginatedResponse(
        items=classifications,
        **params.to_page_response(total)
    )


@router.get("/source/{agn_id}", response_model=APIResponse)
async def get_classification_by_source(
    agn_id: int = Path(..., description="AGN source ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get classification for a specific source.
    
    Args:
        agn_id: AGN source ID
        db: Database session
        
    Returns:
        Classification for the source
    """
    classification = await classification_repo.get_by_agn_id(db, agn_id)
    
    if not classification:
        return APIResponse(
            success=True,
            message=f"No classification found for source with ID {agn_id}",
            data=None
        )
    
    return APIResponse(
        success=True,
        message=f"Retrieved classification for source with ID {agn_id}",
        data=classification
    )


@router.get("/spec-class/{spec_class}", response_model=PaginatedResponse[Classification])
async def get_classifications_by_spec_class(
    spec_class: str = Path(..., description="Spectroscopic classification"),
    params: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get classifications with a specific spectroscopic class.
    
    Args:
        spec_class: Spectroscopic classification
        params: Pagination parameters
        db: Database session
        
    Returns:
        Paginated list of classifications with the specified spectroscopic class
    """
    classifications = await classification_repo.get_by_spec_class(
        db, spec_class, params.skip, params.limit
    )
    
    # For simplicity, we'll approximate total count
    total = len(classifications) if len(classifications) < params.limit else params.limit + params.skip
    
    return PaginatedResponse(
        items=classifications,
        **params.to_page_response(total)
    )


@router.get("/best-class/{best_class}", response_model=PaginatedResponse[Classification])
async def get_classifications_by_best_class(
    best_class: str = Path(..., description="Best classification"),
    params: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get classifications with a specific best class.
    
    Args:
        best_class: Best classification
        params: Pagination parameters
        db: Database session
        
    Returns:
        Paginated list of classifications with the specified best class
    """
    classifications = await classification_repo.get_by_best_class(
        db, best_class, params.skip, params.limit
    )
    
    # For simplicity, we'll approximate total count
    total = len(classifications) if len(classifications) < params.limit else params.limit + params.skip
    
    return PaginatedResponse(
        items=classifications,
        **params.to_page_response(total)
    )


@router.get("/distribution/{class_field}", response_model=APIResponse)
async def get_class_distribution(
    class_field: str = Path(..., description="Classification field to get distribution for"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get distribution of classifications for a specific field.
    
    Args:
        class_field: Classification field to get distribution for
            (spec_class, gen_class, best_class, etc.)
        db: Database session
        
    Returns:
        Distribution of classifications
    """
    try:
        distribution = await classification_repo.get_class_distribution(db, class_field)
        
        return APIResponse(
            success=True,
            message=f"Retrieved distribution for {class_field}",
            data={"distribution": distribution}
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/multiple-types", response_model=PaginatedResponse[Classification])
async def get_classifications_with_multiple_types(
    params: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get classifications that have multiple classification types specified.
    
    Args:
        params: Pagination parameters
        db: Database session
        
    Returns:
        Paginated list of classifications with multiple classification types
    """
    classifications = await classification_repo.get_classifications_with_multiple_types(
        db, params.skip, params.limit
    )
    
    # For simplicity, we'll approximate total count
    total = len(classifications) if len(classifications) < params.limit else params.limit + params.skip
    
    return PaginatedResponse(
        items=classifications,
        **params.to_page_response(total)
    )


@router.get("/{class_id}", response_model=APIResponse)
async def get_classification_by_id(
    class_id: int = Path(..., description="Classification ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a classification by ID.
    
    Args:
        class_id: Classification ID
        db: Database session
        
    Returns:
        Classification with the specified ID
        
    Raises:
        NotFoundException: If classification not found
    """
    classification = await classification_repo.get_by_class_id(db, class_id)
    
    if not classification:
        raise NotFoundException(f"Classification with ID {class_id} not found")
    
    return APIResponse(
        success=True,
        message=f"Retrieved classification with ID {class_id}",
        data=classification
    ) 