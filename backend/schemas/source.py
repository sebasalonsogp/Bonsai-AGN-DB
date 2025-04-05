from typing import Optional, List
from pydantic import Field, confloat

from .base import BaseSchema, BaseDBSchema, PaginationParams


class SourceBase(BaseSchema):
    """Base schema for source AGN data."""
    
    ra: confloat(ge=0.0, lt=360.0) = Field(..., description="Right ascension in degrees")
    declination: confloat(ge=-90.0, le=90.0) = Field(..., description="Declination in degrees")


class SourceCreate(SourceBase):
    """Schema for creating a new source AGN."""
    pass


class SourceUpdate(BaseSchema):
    """Schema for updating an existing source AGN."""
    
    ra: Optional[confloat(ge=0.0, lt=360.0)] = Field(None, description="Right ascension in degrees")
    declination: Optional[confloat(ge=-90.0, le=90.0)] = Field(None, description="Declination in degrees")


class SourceInDB(SourceBase, BaseDBSchema):
    """Schema for source AGN data from database."""
    
    agn_id: int = Field(..., description="Unique AGN identifier")


class Source(SourceInDB):
    """Schema for source AGN data returned by API."""
    pass


class SourceDetail(Source):
    """Schema for detailed source AGN data with relationships."""
    
    # These would be populated from relationships
    # photometry: List["PhotometryInDB"] = []
    # redshift_measurements: List["RedshiftMeasurementInDB"] = []
    # classifications: List["ClassificationInDB"] = []
    pass


class SourceSearchParams(PaginationParams):
    """Query parameters for source AGN search."""
    
    ra: Optional[float] = Field(None, description="Right ascension in degrees")
    declination: Optional[float] = Field(None, description="Declination in degrees")
    radius: Optional[float] = Field(None, gt=0, description="Search radius in degrees")


class CoordinateSearchParams(PaginationParams):
    """Query parameters for searching sources by coordinates and radius."""
    
    ra: float = Field(..., description="Right ascension in degrees")
    declination: float = Field(..., description="Declination in degrees")
    radius: float = Field(0.1, gt=0, description="Search radius in degrees") 