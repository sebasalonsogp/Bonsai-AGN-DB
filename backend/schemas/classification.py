from typing import Optional, List
from pydantic import Field

from .base import BaseSchema, BaseDBSchema, PaginationParams


class ClassificationBase(BaseSchema):
    """Base schema for classification data."""
    
    agn_id: int = Field(..., description="AGN source identifier")
    spec_class: Optional[str] = Field(None, description="Spectroscopic classification")
    gen_class: Optional[str] = Field(None, description="General classification")
    xray_class: Optional[str] = Field(None, description="X-ray classification")
    best_class: Optional[str] = Field(None, description="Best classification")
    image_class: Optional[str] = Field(None, description="Image-based classification")
    sed_class: Optional[str] = Field(None, description="SED-based classification")


class ClassificationCreate(ClassificationBase):
    """Schema for creating a new classification."""
    pass


class ClassificationUpdate(BaseSchema):
    """Schema for updating an existing classification."""
    
    spec_class: Optional[str] = Field(None, description="Spectroscopic classification")
    gen_class: Optional[str] = Field(None, description="General classification")
    xray_class: Optional[str] = Field(None, description="X-ray classification")
    best_class: Optional[str] = Field(None, description="Best classification")
    image_class: Optional[str] = Field(None, description="Image-based classification")
    sed_class: Optional[str] = Field(None, description="SED-based classification")


class ClassificationInDB(ClassificationBase, BaseDBSchema):
    """Schema for classification data from database."""
    
    class_id: int = Field(..., description="Unique classification identifier")


class Classification(ClassificationInDB):
    """Schema for classification data returned by API."""
    pass


class ClassificationSearchParams(PaginationParams):
    """Query parameters for classification search."""
    
    agn_id: Optional[int] = Field(None, description="AGN source identifier")
    spec_class: Optional[str] = Field(None, description="Spectroscopic classification")
    gen_class: Optional[str] = Field(None, description="General classification")
    xray_class: Optional[str] = Field(None, description="X-ray classification")
    best_class: Optional[str] = Field(None, description="Best classification")
    image_class: Optional[str] = Field(None, description="Image-based classification")
    sed_class: Optional[str] = Field(None, description="SED-based classification") 