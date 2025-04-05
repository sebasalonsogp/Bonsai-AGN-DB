from typing import List, Optional, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from database.models import Classification
from schemas.classification import ClassificationCreate, ClassificationUpdate


class ClassificationRepository(BaseRepository[Classification, ClassificationCreate, ClassificationUpdate]):
    """Repository for Classification model operations."""
    
    def __init__(self):
        """Initialize with Classification model."""
        super().__init__(Classification)
    
    async def get_by_class_id(self, db: AsyncSession, class_id: int) -> Optional[Classification]:
        """Get classification by ID.
        
        Args:
            db: Database session
            class_id: Classification ID
            
        Returns:
            Classification instance or None if not found
        """
        query = select(self.model).where(self.model.class_id == class_id)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_by_agn_id(self, db: AsyncSession, agn_id: int) -> Optional[Classification]:
        """Get classification for a specific source.
        
        Args:
            db: Database session
            agn_id: AGN source ID
            
        Returns:
            Classification instance or None if not found
        """
        query = select(self.model).where(self.model.agn_id == agn_id)
        result = await db.execute(query)
        return result.scalars().first()  # There should be only one classification per source
    
    async def get_by_spec_class(
        self, 
        db: AsyncSession, 
        spec_class: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Classification]:
        """Get classifications by spectroscopic class.
        
        Args:
            db: Database session
            spec_class: Spectroscopic classification
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Classification instances with the specified spectroscopic class
        """
        query = (
            select(self.model)
            .where(self.model.spec_class == spec_class)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_gen_class(
        self, 
        db: AsyncSession, 
        gen_class: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Classification]:
        """Get classifications by general class.
        
        Args:
            db: Database session
            gen_class: General classification
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Classification instances with the specified general class
        """
        query = (
            select(self.model)
            .where(self.model.gen_class == gen_class)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_best_class(
        self, 
        db: AsyncSession, 
        best_class: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Classification]:
        """Get classifications by best class.
        
        Args:
            db: Database session
            best_class: Best classification
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Classification instances with the specified best class
        """
        query = (
            select(self.model)
            .where(self.model.best_class == best_class)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_class_distribution(
        self, 
        db: AsyncSession,
        class_field: str = "best_class"
    ) -> Dict[str, int]:
        """Get distribution of classifications.
        
        Args:
            db: Database session
            class_field: Classification field to get distribution for
                (spec_class, gen_class, best_class, etc.)
            
        Returns:
            Dictionary mapping class values to counts
        """
        if class_field not in [
            "spec_class", "gen_class", "xray_class", 
            "best_class", "image_class", "sed_class"
        ]:
            raise ValueError(f"Invalid class field: {class_field}")
        
        # Get column to query based on class_field
        column = getattr(self.model, class_field)
        
        # Query for the distribution
        query = (
            select(column, func.count(column))
            .group_by(column)
            .order_by(func.count(column).desc())
        )
        result = await db.execute(query)
        
        # Return dictionary mapping class values to counts
        return {class_name: count for class_name, count in result.all() if class_name is not None}
    
    async def get_classifications_with_multiple_types(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[Classification]:
        """Get classifications that have multiple classification types specified.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Classification instances with multiple classification types
        """
        # This query finds sources that have more than one classification type specified
        query = (
            select(self.model)
            .where(
                (self.model.spec_class != None) | 
                (self.model.gen_class != None) | 
                (self.model.xray_class != None) | 
                (self.model.image_class != None) | 
                (self.model.sed_class != None)
            )
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all() 