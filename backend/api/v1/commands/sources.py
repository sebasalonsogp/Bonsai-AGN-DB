from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundException, ValidationException
from database import get_db_session
from repositories.source_repository import SourceRepository
from schemas import (
    SourceCreate, 
    SourceUpdate, 
    Source, 
    APIResponse
)

# Create router for source commands
router = APIRouter(prefix="/sources", tags=["Sources"])

# Create repository instance
source_repo = SourceRepository()


@router.post("/", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def create_source(
    source_in: SourceCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Create a new source.
    
    Args:
        source_in: Source creation data
        db: Database session
        
    Returns:
        Created source
        
    Raises:
        ValidationException: If validation fails
    """
    # Create source
    source = await source_repo.create(db, source_in)
    
    return APIResponse(
        success=True,
        message="Source created successfully",
        data=source
    )


@router.put("/{agn_id}", response_model=APIResponse)
async def update_source(
    source_in: SourceUpdate,
    agn_id: int = Path(..., description="AGN ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Update a source.
    
    Args:
        source_in: Source update data
        agn_id: AGN ID
        db: Database session
        
    Returns:
        Updated source
        
    Raises:
        NotFoundException: If source not found
        ValidationException: If validation fails
    """
    # Check if empty update
    if not source_in.model_dump(exclude_unset=True):
        raise ValidationException("No fields to update")
    
    # Update source
    source = await source_repo.update(db, id=agn_id, obj_in=source_in)
    
    return APIResponse(
        success=True,
        message=f"Source with ID {agn_id} updated successfully",
        data=source
    )


@router.delete("/{agn_id}", response_model=APIResponse)
async def delete_source(
    agn_id: int = Path(..., description="AGN ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete a source.
    
    Args:
        agn_id: AGN ID
        db: Database session
        
    Returns:
        Deleted source ID
        
    Raises:
        NotFoundException: If source not found
    """
    # Delete source
    await source_repo.delete(db, id=agn_id)
    
    return APIResponse(
        success=True,
        message=f"Source with ID {agn_id} deleted successfully",
        data={"agn_id": agn_id}
    ) 