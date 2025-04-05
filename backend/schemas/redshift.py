from typing import Optional, List
from pydantic import Field, confloat

from .base import BaseSchema, BaseDBSchema, PaginationParams


class RedshiftBase(BaseSchema):
    """Base schema for redshift measurement data."""
    
    agn_id: int = Field(..., description="AGN source identifier")
    redshift_type: str = Field(..., description="Type of redshift measurement")
    z_value: confloat(ge=0.0) = Field(..., description="Redshift value")
    z_error: Optional[confloat(ge=0.0)] = Field(None, description="Error on redshift measurement")


class RedshiftCreate(RedshiftBase):
    """Schema for creating a new redshift measurement."""
    pass


class RedshiftUpdate(BaseSchema):
    """Schema for updating an existing redshift measurement."""
    
    redshift_type: Optional[str] = Field(None, description="Type of redshift measurement")
    z_value: Optional[confloat(ge=0.0)] = Field(None, description="Redshift value")
    z_error: Optional[confloat(ge=0.0)] = Field(None, description="Error on redshift measurement")


class RedshiftInDB(RedshiftBase, BaseDBSchema):
    """Schema for redshift measurement data from database."""
    
    redshift_id: int = Field(..., description="Unique redshift measurement identifier")


class Redshift(RedshiftInDB):
    """Schema for redshift measurement data returned by API."""
    pass


class RedshiftSearchParams(PaginationParams):
    """Query parameters for redshift measurement search."""
    
    agn_id: Optional[int] = Field(None, description="AGN source identifier")
    redshift_type: Optional[str] = Field(None, description="Type of redshift measurement")
    min_z: Optional[float] = Field(None, ge=0.0, description="Minimum redshift value")
    max_z: Optional[float] = Field(None, ge=0.0, description="Maximum redshift value") 