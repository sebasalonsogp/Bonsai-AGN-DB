from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundException, ValidationException, DatabaseException
from database import get_db_session
from repositories.classification_repository import ClassificationRepository
from repositories.source_repository import SourceRepository
from schemas import (
    ClassificationCreate, 
    ClassificationUpdate, 
    Classification, 
    APIResponse
)

# Create router for classification commands
router = APIRouter(prefix="/classification", tags=["Classification"])

# Create repository instances
classification_repo = ClassificationRepository()
source_repo = SourceRepository()


@router.post("/", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def create_classification(
    classification_in: ClassificationCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Create a new classification.
    
    Args:
        classification_in: Classification creation data
        db: Database session
        
    Returns:
        Created classification
        
    Raises:
        ValidationException: If validation fails or source does not exist
    """
    # Verify that the source exists
    source = await source_repo.get_by_agn_id(db, classification_in.agn_id)
    if not source:
        raise ValidationException(f"Source with ID {classification_in.agn_id} does not exist")
    
    # Check if a classification already exists for this source
    existing_classification = await classification_repo.get_by_agn_id(db, classification_in.agn_id)
    if existing_classification:
        raise ValidationException(f"Classification already exists for source with ID {classification_in.agn_id}")
    
    # Create classification
    try:
        classification = await classification_repo.create(db, classification_in)
        
        return APIResponse(
            success=True,
            message="Classification created successfully",
            data=classification
        )
    except Exception as e:
        # Log the exception
        raise DatabaseException(f"Failed to create classification: {str(e)}")


@router.put("/{class_id}", response_model=APIResponse)
async def update_classification(
    classification_in: ClassificationUpdate,
    class_id: int = Path(..., description="Classification ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Update a classification.
    
    Args:
        classification_in: Classification update data
        class_id: Classification ID
        db: Database session
        
    Returns:
        Updated classification
        
    Raises:
        NotFoundException: If classification not found
        ValidationException: If validation fails or source does not exist
    """
    # Check if empty update
    if not classification_in.model_dump(exclude_unset=True):
        raise ValidationException("No fields to update")
    
    # If updating agn_id, verify that the source exists and has no existing classification
    if classification_in.agn_id is not None:
        source = await source_repo.get_by_agn_id(db, classification_in.agn_id)
        if not source:
            raise ValidationException(f"Source with ID {classification_in.agn_id} does not exist")
        
        # Check if this source already has a different classification
        existing_classification = await classification_repo.get_by_agn_id(db, classification_in.agn_id)
        if existing_classification and existing_classification.class_id != class_id:
            raise ValidationException(f"Source with ID {classification_in.agn_id} already has a classification")
    
    # Verify classification exists
    classification = await classification_repo.get_by_class_id(db, class_id)
    if not classification:
        raise NotFoundException(f"Classification with ID {class_id} not found")
    
    # Update classification
    try:
        updated_classification = await classification_repo.update(db, id=class_id, obj_in=classification_in)
        
        return APIResponse(
            success=True,
            message=f"Classification with ID {class_id} updated successfully",
            data=updated_classification
        )
    except NotFoundException:
        raise
    except Exception as e:
        # Log the exception
        raise DatabaseException(f"Failed to update classification: {str(e)}")


@router.delete("/{class_id}", response_model=APIResponse)
async def delete_classification(
    class_id: int = Path(..., description="Classification ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete a classification.
    
    Args:
        class_id: Classification ID
        db: Database session
        
    Returns:
        Deleted classification ID
        
    Raises:
        NotFoundException: If classification not found
    """
    # Verify classification exists
    classification = await classification_repo.get_by_class_id(db, class_id)
    if not classification:
        raise NotFoundException(f"Classification with ID {class_id} not found")
    
    # Delete classification
    try:
        await classification_repo.delete(db, id=class_id)
        
        return APIResponse(
            success=True,
            message=f"Classification with ID {class_id} deleted successfully",
            data={"class_id": class_id}
        )
    except NotFoundException:
        raise
    except Exception as e:
        # Log the exception
        raise DatabaseException(f"Failed to delete classification: {str(e)}") 