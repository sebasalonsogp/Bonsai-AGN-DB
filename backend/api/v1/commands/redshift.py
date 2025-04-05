from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundException, ValidationException, DatabaseException
from database import get_db_session
from repositories.redshift_repository import RedshiftRepository
from repositories.source_repository import SourceRepository
from schemas import (
    RedshiftCreate, 
    RedshiftUpdate, 
    Redshift, 
    APIResponse
)

# Create router for redshift commands
router = APIRouter(prefix="/redshift", tags=["Redshift"])

# Create repository instances
redshift_repo = RedshiftRepository()
source_repo = SourceRepository()


@router.post("/", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def create_redshift(
    redshift_in: RedshiftCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Create a new redshift measurement.
    
    Args:
        redshift_in: Redshift creation data
        db: Database session
        
    Returns:
        Created redshift measurement
        
    Raises:
        ValidationException: If validation fails or source does not exist
    """
    # Verify that the source exists
    source = await source_repo.get_by_agn_id(db, redshift_in.agn_id)
    if not source:
        raise ValidationException(f"Source with ID {redshift_in.agn_id} does not exist")
    
    # Create redshift
    try:
        redshift = await redshift_repo.create(db, redshift_in)
        
        return APIResponse(
            success=True,
            message="Redshift measurement created successfully",
            data=redshift
        )
    except Exception as e:
        # Log the exception
        raise DatabaseException(f"Failed to create redshift measurement: {str(e)}")


@router.put("/{redshift_id}", response_model=APIResponse)
async def update_redshift(
    redshift_in: RedshiftUpdate,
    redshift_id: int = Path(..., description="Redshift measurement ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Update a redshift measurement.
    
    Args:
        redshift_in: Redshift update data
        redshift_id: Redshift measurement ID
        db: Database session
        
    Returns:
        Updated redshift measurement
        
    Raises:
        NotFoundException: If redshift measurement not found
        ValidationException: If validation fails or source does not exist
    """
    # Check if empty update
    if not redshift_in.model_dump(exclude_unset=True):
        raise ValidationException("No fields to update")
    
    # If updating agn_id, verify that the source exists
    if redshift_in.agn_id is not None:
        source = await source_repo.get_by_agn_id(db, redshift_in.agn_id)
        if not source:
            raise ValidationException(f"Source with ID {redshift_in.agn_id} does not exist")
    
    # Verify redshift exists
    redshift = await redshift_repo.get_by_redshift_id(db, redshift_id)
    if not redshift:
        raise NotFoundException(f"Redshift measurement with ID {redshift_id} not found")
    
    # Update redshift
    try:
        updated_redshift = await redshift_repo.update(db, id=redshift_id, obj_in=redshift_in)
        
        return APIResponse(
            success=True,
            message=f"Redshift measurement with ID {redshift_id} updated successfully",
            data=updated_redshift
        )
    except NotFoundException:
        raise
    except Exception as e:
        # Log the exception
        raise DatabaseException(f"Failed to update redshift measurement: {str(e)}")


@router.delete("/{redshift_id}", response_model=APIResponse)
async def delete_redshift(
    redshift_id: int = Path(..., description="Redshift measurement ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete a redshift measurement.
    
    Args:
        redshift_id: Redshift measurement ID
        db: Database session
        
    Returns:
        Deleted redshift measurement ID
        
    Raises:
        NotFoundException: If redshift measurement not found
    """
    # Verify redshift exists
    redshift = await redshift_repo.get_by_redshift_id(db, redshift_id)
    if not redshift:
        raise NotFoundException(f"Redshift measurement with ID {redshift_id} not found")
    
    # Delete redshift
    try:
        await redshift_repo.delete(db, id=redshift_id)
        
        return APIResponse(
            success=True,
            message=f"Redshift measurement with ID {redshift_id} deleted successfully",
            data={"redshift_id": redshift_id}
        )
    except NotFoundException:
        raise
    except Exception as e:
        # Log the exception
        raise DatabaseException(f"Failed to delete redshift measurement: {str(e)}")


@router.post("/batch", response_model=APIResponse)
async def create_batch_redshifts(
    redshift_batch: list[RedshiftCreate],
    db: AsyncSession = Depends(get_db_session)
):
    """
    Create multiple redshift measurements in a batch.
    
    Args:
        redshift_batch: List of redshift creation data
        db: Database session
        
    Returns:
        Count of created redshift measurements
        
    Raises:
        ValidationException: If validation fails or a source does not exist
    """
    if not redshift_batch:
        raise ValidationException("Batch is empty")
    
    # Collect all unique source IDs
    source_ids = set(item.agn_id for item in redshift_batch)
    
    # Verify that all sources exist
    for agn_id in source_ids:
        source = await source_repo.get_by_agn_id(db, agn_id)
        if not source:
            raise ValidationException(f"Source with ID {agn_id} does not exist")
    
    # Create redshift measurements
    created_redshifts = []
    try:
        for redshift_in in redshift_batch:
            redshift = await redshift_repo.create(db, redshift_in)
            created_redshifts.append(redshift)
        
        return APIResponse(
            success=True,
            message=f"Created {len(created_redshifts)} redshift measurements successfully",
            data={"count": len(created_redshifts)}
        )
    except Exception as e:
        # Log the exception
        await db.rollback()
        raise DatabaseException(f"Failed to create batch redshift measurements: {str(e)}") 