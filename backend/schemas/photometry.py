from typing import Optional, List
from pydantic import Field, validator

from .base import BaseSchema, BaseDBSchema, PaginationParams


class PhotometryBase(BaseSchema):
    """Base schema for photometry measurement data."""
    
    agn_id: int = Field(..., description="AGN source ID")
    band_label: str = Field(..., description="Photometric band label")
    filter_name: str = Field(..., description="Filter name")
    mag_value: Optional[float] = Field(None, description="Magnitude value")
    mag_error: Optional[float] = Field(None, description="Magnitude error")
    extinction: Optional[float] = Field(None, description="Extinction value")
    
    @validator('mag_error')
    def error_must_be_positive(cls, v):
        """Validate that magnitude error is positive if provided."""
        if v is not None and v <= 0:
            raise ValueError('Magnitude error must be positive')
        return v


class PhotometryCreate(PhotometryBase):
    """Schema for creating a new photometry measurement."""
    pass


class PhotometryUpdate(BaseSchema):
    """Schema for updating an existing photometry measurement."""
    
    agn_id: Optional[int] = Field(None, description="AGN source ID")
    band_label: Optional[str] = Field(None, description="Photometric band label")
    filter_name: Optional[str] = Field(None, description="Filter name")
    mag_value: Optional[float] = Field(None, description="Magnitude value")
    mag_error: Optional[float] = Field(None, description="Magnitude error")
    extinction: Optional[float] = Field(None, description="Extinction value")
    
    @validator('mag_error')
    def error_must_be_positive(cls, v):
        """Validate that magnitude error is positive if provided."""
        if v is not None and v <= 0:
            raise ValueError('Magnitude error must be positive')
        return v


class PhotometryInDB(PhotometryBase, BaseDBSchema):
    """Schema for photometry measurement data from database."""
    
    phot_id: int = Field(..., description="Unique photometry measurement identifier")


class Photometry(PhotometryInDB):
    """Schema for photometry measurement data returned by API."""
    pass


class PhotometrySearchParams(PaginationParams):
    """Query parameters for photometry search."""
    
    agn_id: Optional[int] = Field(None, description="AGN source ID")
    band_label: Optional[str] = Field(None, description="Photometric band label")
    filter_name: Optional[str] = Field(None, description="Filter name")
    min_mag: Optional[float] = Field(None, description="Minimum magnitude value")
    max_mag: Optional[float] = Field(None, description="Maximum magnitude value")


class BandSearchParams(PaginationParams):
    """Query parameters for searching by band."""
    
    band_label: str = Field(..., description="Photometric band label")


class FilterSearchParams(PaginationParams):
    """Query parameters for searching by filter."""
    
    filter_name: str = Field(..., description="Filter name")


class MagnitudeRangeParams(PaginationParams):
    """Query parameters for searching by magnitude range."""
    
    min_mag: Optional[float] = Field(None, description="Minimum magnitude value")
    max_mag: Optional[float] = Field(None, description="Maximum magnitude value") 