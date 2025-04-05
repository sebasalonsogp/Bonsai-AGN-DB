from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundException, ValidationException, DatabaseException
from database import get_db_session
from repositories.photometry_repository import PhotometryRepository
from repositories.source_repository import SourceRepository
from schemas import (
    PhotometryCreate, 
    PhotometryUpdate, 
    Photometry, 
    APIResponse
)

# Create router for photometry commands
router = APIRouter(prefix="/photometry", tags=["Photometry"])

# Create repository instances
photometry_repo = PhotometryRepository()
source_repo = SourceRepository()


@router.post("/", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def create_photometry(
    photometry_in: PhotometryCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Create a new photometry measurement.
    
    Args:
        photometry_in: Photometry creation data
        db: Database session
        
    Returns:
        Created photometry measurement
        
    Raises:
        ValidationException: If validation fails or source does not exist
    """
    # Verify that the source exists
    source = await source_repo.get_by_agn_id(db, photometry_in.agn_id)
    if not source:
        raise ValidationException(f"Source with ID {photometry_in.agn_id} does not exist")
    
    # Create photometry
    try:
        photometry = await photometry_repo.create(db, photometry_in)
        
        return APIResponse(
            success=True,
            message="Photometry measurement created successfully",
            data=photometry
        )
    except Exception as e:
        # Log the exception
        raise DatabaseException(f"Failed to create photometry measurement: {str(e)}")


@router.put("/{phot_id}", response_model=APIResponse)
async def update_photometry(
    photometry_in: PhotometryUpdate,
    phot_id: int = Path(..., description="Photometry measurement ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Update a photometry measurement.
    
    Args:
        photometry_in: Photometry update data
        phot_id: Photometry measurement ID
        db: Database session
        
    Returns:
        Updated photometry measurement
        
    Raises:
        NotFoundException: If photometry measurement not found
        ValidationException: If validation fails or source does not exist
    """
    # Check if empty update
    if not photometry_in.model_dump(exclude_unset=True):
        raise ValidationException("No fields to update")
    
    # If updating agn_id, verify that the source exists
    if photometry_in.agn_id is not None:
        source = await source_repo.get_by_agn_id(db, photometry_in.agn_id)
        if not source:
            raise ValidationException(f"Source with ID {photometry_in.agn_id} does not exist")
    
    # Update photometry
    try:
        photometry = await photometry_repo.update(db, id=phot_id, obj_in=photometry_in)
        
        return APIResponse(
            success=True,
            message=f"Photometry measurement with ID {phot_id} updated successfully",
            data=photometry
        )
    except NotFoundException:
        raise
    except Exception as e:
        # Log the exception
        raise DatabaseException(f"Failed to update photometry measurement: {str(e)}")


@router.delete("/{phot_id}", response_model=APIResponse)
async def delete_photometry(
    phot_id: int = Path(..., description="Photometry measurement ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete a photometry measurement.
    
    Args:
        phot_id: Photometry measurement ID
        db: Database session
        
    Returns:
        Deleted photometry measurement ID
        
    Raises:
        NotFoundException: If photometry measurement not found
    """
    # Delete photometry
    try:
        photometry = await photometry_repo.delete(db, id=phot_id)
        
        return APIResponse(
            success=True,
            message=f"Photometry measurement with ID {phot_id} deleted successfully",
            data={"phot_id": phot_id}
        )
    except NotFoundException:
        raise
    except Exception as e:
        # Log the exception
        raise DatabaseException(f"Failed to delete photometry measurement: {str(e)}")


@router.post("/batch", response_model=APIResponse)
async def create_batch_photometry(
    photometry_batch: list[PhotometryCreate],
    db: AsyncSession = Depends(get_db_session)
):
    """
    Create multiple photometry measurements in a batch.
    
    Args:
        photometry_batch: List of photometry creation data
        db: Database session
        
    Returns:
        Count of created photometry measurements
        
    Raises:
        ValidationException: If validation fails or a source does not exist
    """
    if not photometry_batch:
        raise ValidationException("Batch is empty")
    
    # Collect all unique source IDs
    source_ids = set(item.agn_id for item in photometry_batch)
    
    # Verify that all sources exist
    for agn_id in source_ids:
        source = await source_repo.get_by_agn_id(db, agn_id)
        if not source:
            raise ValidationException(f"Source with ID {agn_id} does not exist")
    
    # Create photometry measurements
    created_photometry = []
    try:
        for photometry_in in photometry_batch:
            photometry = await photometry_repo.create(db, photometry_in)
            created_photometry.append(photometry)
        
        return APIResponse(
            success=True,
            message=f"Created {len(created_photometry)} photometry measurements successfully",
            data={"count": len(created_photometry)}
        )
    except Exception as e:
        # Log the exception
        await db.rollback()
        raise DatabaseException(f"Failed to create batch photometry measurements: {str(e)}") 