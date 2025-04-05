from typing import List, Optional, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from database.models import RedshiftMeasurement
from schemas.redshift import RedshiftCreate, RedshiftUpdate


class RedshiftRepository(BaseRepository[RedshiftMeasurement, RedshiftCreate, RedshiftUpdate]):
    """Repository for RedshiftMeasurement model operations."""
    
    def __init__(self):
        """Initialize with RedshiftMeasurement model."""
        super().__init__(RedshiftMeasurement)
    
    async def get_by_redshift_id(self, db: AsyncSession, redshift_id: int) -> Optional[RedshiftMeasurement]:
        """Get redshift measurement by ID.
        
        Args:
            db: Database session
            redshift_id: Redshift measurement ID
            
        Returns:
            RedshiftMeasurement instance or None if not found
        """
        query = select(self.model).where(self.model.redshift_id == redshift_id)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_by_agn_id(self, db: AsyncSession, agn_id: int) -> List[RedshiftMeasurement]:
        """Get redshift measurements for a specific source.
        
        Args:
            db: Database session
            agn_id: AGN source ID
            
        Returns:
            List of RedshiftMeasurement instances for the source
        """
        query = select(self.model).where(self.model.agn_id == agn_id)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_redshift_type(
        self, 
        db: AsyncSession, 
        redshift_type: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[RedshiftMeasurement]:
        """Get redshift measurements by type.
        
        Args:
            db: Database session
            redshift_type: Type of redshift measurement
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of RedshiftMeasurement instances with the specified type
        """
        query = (
            select(self.model)
            .where(self.model.redshift_type == redshift_type)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_redshift_range(
        self, 
        db: AsyncSession, 
        min_z: Optional[float] = None,
        max_z: Optional[float] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[RedshiftMeasurement]:
        """Get redshift measurements within a redshift range.
        
        Args:
            db: Database session
            min_z: Minimum redshift value (inclusive)
            max_z: Maximum redshift value (inclusive)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of RedshiftMeasurement instances within the redshift range
        """
        query = select(self.model)
        
        if min_z is not None:
            query = query.where(self.model.z_value >= min_z)
        
        if max_z is not None:
            query = query.where(self.model.z_value <= max_z)
            
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_redshift_types_for_source(self, db: AsyncSession, agn_id: int) -> List[str]:
        """Get all unique redshift types for a source.
        
        Args:
            db: Database session
            agn_id: AGN source ID
            
        Returns:
            List of unique redshift types
        """
        query = (
            select(self.model.redshift_type)
            .distinct()
            .where(self.model.agn_id == agn_id)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_average_redshift(self, db: AsyncSession, agn_id: int) -> Optional[float]:
        """Get the average redshift for a source.
        
        Args:
            db: Database session
            agn_id: AGN source ID
            
        Returns:
            Average redshift value or None if no measurements exist
        """
        query = (
            select(func.avg(self.model.z_value))
            .where(self.model.agn_id == agn_id)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_statistics(self, db: AsyncSession, redshift_type: Optional[str] = None) -> Dict[str, Any]:
        """Get statistics for redshift data.
        
        Args:
            db: Database session
            redshift_type: Optional redshift type to limit statistics to a specific type
            
        Returns:
            Dictionary with statistics (count, avg_z, avg_error, etc.)
        """
        # Start with a base query
        count_query = select(func.count()).select_from(self.model)
        avg_z_query = select(func.avg(self.model.z_value))
        avg_error_query = select(func.avg(self.model.z_error))
        min_z_query = select(func.min(self.model.z_value))
        max_z_query = select(func.max(self.model.z_value))
        
        # Apply filter if redshift_type is provided
        if redshift_type is not None:
            count_query = count_query.where(self.model.redshift_type == redshift_type)
            avg_z_query = avg_z_query.where(self.model.redshift_type == redshift_type)
            avg_error_query = avg_error_query.where(self.model.redshift_type == redshift_type)
            min_z_query = min_z_query.where(self.model.redshift_type == redshift_type)
            max_z_query = max_z_query.where(self.model.redshift_type == redshift_type)
        
        # Execute queries
        count_result = await db.execute(count_query)
        avg_z_result = await db.execute(avg_z_query)
        avg_error_result = await db.execute(avg_error_query)
        min_z_result = await db.execute(min_z_query)
        max_z_result = await db.execute(max_z_query)
        
        # Return statistics
        return {
            "count": count_result.scalar_one(),
            "avg_redshift": avg_z_result.scalar_one(),
            "avg_error": avg_error_result.scalar_one(),
            "min_redshift": min_z_result.scalar_one(),
            "max_redshift": max_z_result.scalar_one()
        } 