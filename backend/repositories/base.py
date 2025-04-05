from typing import Generic, TypeVar, Type, List, Optional, Any, Dict, Union
from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Select

from core.exceptions import DatabaseException, NotFoundException
from database.models import Base

# Type variables for generic repository
ModelType = TypeVar("ModelType", bound=Base)  # SQLAlchemy model type
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)  # Pydantic schema for creation operations
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)  # Pydantic schema for update operations


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base repository with CRUD operations for database models.
    
    Implements the Repository Pattern for a clean separation between
    data access logic and business logic. This abstract base class provides
    common database operations that specific repositories can inherit.
    
    Following Clean Architecture principles, this repository layer:
    - Encapsulates all database access logic
    - Provides a consistent interface for data operations
    - Isolates the rest of the application from database implementation details
    - Facilitates testing by allowing mocked repositories
    
    Type Parameters:
        ModelType: The SQLAlchemy model class this repository works with
        CreateSchemaType: Pydantic schema for creation operations
        UpdateSchemaType: Pydantic schema for update operations
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize repository with a SQLAlchemy model.
        
        Args:
            model: SQLAlchemy model class that this repository will operate on
        """
        self.model = model
    
    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new database record.
        
        Converts a Pydantic schema to a SQLAlchemy model instance,
        adds it to the database, and returns the created instance.
        
        Args:
            db: Database session for the transaction
            obj_in: Pydantic schema with creation data
            
        Returns:
            Created database model instance with populated ID
            
        Raises:
            DatabaseException: If creation fails (constraint violation, etc.)
        """
        try:
            # Convert Pydantic model to dict
            obj_in_data = obj_in.model_dump()
            
            # Create SQLAlchemy model instance
            db_obj = self.model(**obj_in_data)
            
            # Add to session and commit
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            
            return db_obj
        except Exception as e:
            await db.rollback()
            raise DatabaseException(f"Failed to create {self.model.__name__}: {str(e)}")
    
    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        Get a record by ID.
        
        Retrieves a single record by its primary key ID.
        
        Args:
            db: Database session
            id: ID of the record to retrieve
            
        Returns:
            Database model instance or None if not found
        """
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_or_404(self, db: AsyncSession, id: Any) -> ModelType:
        """
        Get a record by ID or raise 404 if not found.
        
        Similar to get() but raises an exception if the record doesn't exist,
        useful for API endpoints that need to return 404 responses.
        
        Args:
            db: Database session
            id: ID of the record to retrieve
            
        Returns:
            Database model instance
            
        Raises:
            NotFoundException: If record not found (maps to HTTP 404)
        """
        obj = await self.get(db, id)
        if obj is None:
            raise NotFoundException(f"{self.model.__name__} with id {id} not found")
        return obj
    
    async def get_multi(
        self, 
        db: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        query: Optional[Select] = None
    ) -> List[ModelType]:
        """
        Get multiple records with pagination.
        
        Retrieves a list of records with pagination support.
        Can accept a pre-configured query for filtering.
        
        Args:
            db: Database session
            skip: Number of records to skip (for pagination offset)
            limit: Maximum number of records to return (for pagination size)
            query: Optional pre-configured query for additional filtering
            
        Returns:
            List of database model instances matching the criteria
        """
        if query is None:
            query = select(self.model)
            
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def update(
        self, 
        db: AsyncSession, 
        *, 
        id: Any, 
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update a record.
        
        Updates an existing record with new values from a Pydantic schema
        or dictionary. Only fields present in the update data will be modified.
        
        Args:
            db: Database session
            id: ID of the record to update
            obj_in: Update data as Pydantic schema or dict
            
        Returns:
            Updated database model instance
            
        Raises:
            NotFoundException: If record not found
            DatabaseException: If update fails (constraint violation, etc.)
        """
        try:
            # Get the existing model
            db_obj = await self.get_or_404(db, id)
            
            # Handle input as either Pydantic model or dict
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)
                
            # Create update statement
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(**update_data)
                .execution_options(synchronize_session="fetch")
            )
            
            # Execute update
            await db.execute(stmt)
            await db.commit()
            await db.refresh(db_obj)
            
            return db_obj
        except NotFoundException:
            raise
        except Exception as e:
            await db.rollback()
            raise DatabaseException(f"Failed to update {self.model.__name__}: {str(e)}")
    
    async def delete(self, db: AsyncSession, *, id: Any) -> ModelType:
        """
        Delete a record.
        
        Removes a record from the database by ID. Returns the deleted record
        before it's removed from the database.
        
        Args:
            db: Database session
            id: ID of the record to delete
            
        Returns:
            Deleted database model instance (before deletion)
            
        Raises:
            NotFoundException: If record not found
            DatabaseException: If deletion fails (e.g., due to constraints)
        """
        try:
            # Get the existing model
            db_obj = await self.get_or_404(db, id)
            
            # Create delete statement
            stmt = (
                delete(self.model)
                .where(self.model.id == id)
                .execution_options(synchronize_session="fetch")
            )
            
            # Execute delete
            await db.execute(stmt)
            await db.commit()
            
            return db_obj
        except NotFoundException:
            raise
        except Exception as e:
            await db.rollback()
            raise DatabaseException(f"Failed to delete {self.model.__name__}: {str(e)}")
    
    async def exists(self, db: AsyncSession, id: Any) -> bool:
        """
        Check if a record exists.
        
        Efficiently checks for existence without retrieving the full record,
        useful for validation before operations.
        
        Args:
            db: Database session
            id: ID of the record to check
            
        Returns:
            True if record exists, False otherwise
        """
        query = select(self.model.id).where(self.model.id == id)
        result = await db.execute(query)
        return result.scalar() is not None 