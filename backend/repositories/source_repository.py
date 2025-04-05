from typing import List, Optional, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from .base import BaseRepository
from database.models import SourceAGN
from schemas.source import SourceCreate, SourceUpdate


class SourceRepository(BaseRepository[SourceAGN, SourceCreate, SourceUpdate]):
    """Repository for SourceAGN model operations."""
    
    def __init__(self):
        """Initialize with SourceAGN model."""
        super().__init__(SourceAGN)
    
    async def get_by_agn_id(self, db: AsyncSession, agn_id: int) -> Optional[SourceAGN]:
        """Get source by AGN ID.
        
        Args:
            db: Database session
            agn_id: AGN ID
            
        Returns:
            SourceAGN instance or None if not found
        """
        query = select(self.model).where(self.model.agn_id == agn_id)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def search_by_coordinates(
        self,
        db: AsyncSession,
        ra: float,
        declination: float,
        radius: float = 0.1,
        skip: int = 0,
        limit: int = 100
    ) -> List[SourceAGN]:
        """
        Search sources by coordinates within a radius.
        
        Uses Haversine formula to calculate great-circle distance.
        
        Args:
            db: Database session
            ra: Right ascension in degrees
            declination: Declination in degrees
            radius: Search radius in degrees
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return (pagination)
            
        Returns:
            List of sources within the specified radius
        """
        # Convert to radians for spherical math
        ra_rad = ra * 0.01745329252  # pi/180
        declination_rad = declination * 0.01745329252
        
        # Haversine formula in SQL (MariaDB/MySQL specific)
        stmt = text("""
            SELECT agn_id, ra, declination
            FROM source_agn
            WHERE ACOS(
                sin(:declination_rad) * sin(declination * 0.01745329252) +
                cos(:declination_rad) * cos(declination * 0.01745329252) *
                COS(:ra_rad - ra * 0.01745329252)
            ) * 57.2957795131 <= :radius
            LIMIT :limit OFFSET :skip
        """)
        
        params = {
            "ra_rad": ra_rad,
            "declination_rad": declination_rad,
            "radius": radius,
            "skip": skip,
            "limit": limit
        }
        
        result = await db.execute(stmt, params)
        return result.scalars().all()
    
    async def get_total_count(self, db: AsyncSession) -> int:
        """Get total count of sources.
        
        Args:
            db: Database session
            
        Returns:
            Total count of sources
        """
        query = select(func.count()).select_from(self.model)
        result = await db.execute(query)
        return result.scalar_one()
    
    async def get_by_id_with_related(self, db: AsyncSession, agn_id: int) -> Optional[Dict[str, Any]]:
        """Get source with all related data.
        
        Args:
            db: Database session
            agn_id: AGN ID
            
        Returns:
            Dictionary with source and related data or None if not found
        """
        # Get the source
        source = await self.get_by_agn_id(db, agn_id)
        if not source:
            return None
            
        # Get related data
        source_dict = {
            "source": source,
            "photometry": source.photometry,
            "redshift_measurements": source.redshift_measurements,
            "classifications": source.classifications
        }
        
        return source_dict 