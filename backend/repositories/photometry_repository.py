from typing import List, Optional, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from .base import BaseRepository
from database.models import Photometry
from schemas.photometry import PhotometryCreate, PhotometryUpdate


class PhotometryRepository(BaseRepository[Photometry, PhotometryCreate, PhotometryUpdate]):
    """Repository for Photometry model operations."""
    
    def __init__(self):
        """Initialize with Photometry model."""
        super().__init__(Photometry)
    
    async def get_by_phot_id(self, db: AsyncSession, phot_id: int) -> Optional[Photometry]:
        """Get photometry by ID.
        
        Args:
            db: Database session
            phot_id: Photometry ID
            
        Returns:
            Photometry instance or None if not found
        """
        query = select(self.model).where(self.model.phot_id == phot_id)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_by_agn_id(self, db: AsyncSession, agn_id: int) -> List[Photometry]:
        """Get photometry measurements for a specific source.
        
        Args:
            db: Database session
            agn_id: AGN source ID
            
        Returns:
            List of Photometry instances for the source
        """
        query = select(self.model).where(self.model.agn_id == agn_id)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_band(
        self, 
        db: AsyncSession, 
        band_label: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Photometry]:
        """Get photometry measurements by band.
        
        Args:
            db: Database session
            band_label: Photometric band label (e.g., 'U', 'B', 'V')
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Photometry instances with the specified band
        """
        query = (
            select(self.model)
            .where(self.model.band_label == band_label)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_filter(
        self, 
        db: AsyncSession, 
        filter_name: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Photometry]:
        """Get photometry measurements by filter.
        
        Args:
            db: Database session
            filter_name: Filter name (e.g., 'SDSS u', '2MASS J')
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Photometry instances with the specified filter
        """
        query = (
            select(self.model)
            .where(self.model.filter_name == filter_name)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_magnitude_range(
        self, 
        db: AsyncSession, 
        min_mag: Optional[float] = None,
        max_mag: Optional[float] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Photometry]:
        """Get photometry measurements within a magnitude range.
        
        Args:
            db: Database session
            min_mag: Minimum magnitude value (inclusive)
            max_mag: Maximum magnitude value (inclusive)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Photometry instances within the magnitude range
        """
        query = select(self.model)
        
        if min_mag is not None:
            query = query.where(self.model.mag_value >= min_mag)
        
        if max_mag is not None:
            query = query.where(self.model.mag_value <= max_mag)
            
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_bands_for_source(self, db: AsyncSession, agn_id: int) -> List[str]:
        """Get all unique band labels for a source.
        
        Args:
            db: Database session
            agn_id: AGN source ID
            
        Returns:
            List of unique band labels
        """
        query = (
            select(self.model.band_label)
            .distinct()
            .where(self.model.agn_id == agn_id)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_filters_for_source(self, db: AsyncSession, agn_id: int) -> List[str]:
        """Get all unique filters for a source.
        
        Args:
            db: Database session
            agn_id: AGN source ID
            
        Returns:
            List of unique filter names
        """
        query = (
            select(self.model.filter_name)
            .distinct()
            .where(self.model.agn_id == agn_id)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_statistics(self, db: AsyncSession, agn_id: Optional[int] = None) -> Dict[str, Any]:
        """Get statistics for photometry data.
        
        Args:
            db: Database session
            agn_id: Optional AGN source ID to limit statistics to a specific source
            
        Returns:
            Dictionary with statistics (count, avg_mag, avg_error, etc.)
        """
        # Start with a base query
        count_query = select(func.count()).select_from(self.model)
        avg_mag_query = select(func.avg(self.model.mag_value))
        avg_error_query = select(func.avg(self.model.mag_error))
        avg_extinction_query = select(func.avg(self.model.extinction))
        
        # Apply filter if agn_id is provided
        if agn_id is not None:
            count_query = count_query.where(self.model.agn_id == agn_id)
            avg_mag_query = avg_mag_query.where(self.model.agn_id == agn_id)
            avg_error_query = avg_error_query.where(self.model.agn_id == agn_id)
            avg_extinction_query = avg_extinction_query.where(self.model.agn_id == agn_id)
        
        # Execute queries
        count_result = await db.execute(count_query)
        avg_mag_result = await db.execute(avg_mag_query)
        avg_error_result = await db.execute(avg_error_query)
        avg_extinction_result = await db.execute(avg_extinction_query)
        
        # Return statistics
        return {
            "count": count_result.scalar_one(),
            "avg_magnitude": avg_mag_result.scalar_one(),
            "avg_error": avg_error_result.scalar_one(),
            "avg_extinction": avg_extinction_result.scalar_one()
        } 