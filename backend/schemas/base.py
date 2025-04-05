from datetime import datetime
from typing import Optional, List, Generic, TypeVar, Dict, Any, Type, Union
from pydantic import BaseModel, Field
from enum import Enum


class BaseSchema(BaseModel):
    """Base schema for all models."""
    
    class Config:
        """Pydantic config for all schemas."""
        
        from_attributes = True  # For SQLAlchemy model compatibility
        orm_mode = True
        populate_by_name = True


class BaseDBSchema(BaseSchema):
    """Base schema for database models with timestamps."""
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    id: int


class PaginatedResponse(BaseSchema, Generic[TypeVar('T')]):
    """Paginated response schema with metadata."""
    
    items: List[TypeVar('T')]
    total: int
    page: int
    size: int
    pages: int


class APIResponse(BaseSchema):
    """Standard API response envelope."""
    
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None


class PaginationParams(BaseSchema):
    """Query parameters for pagination."""
    
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(100, ge=1, le=1000, description="Maximum number of records to return")
    sort_field: Optional[str] = Field(None, description="Field to sort by")
    sort_direction: Optional[str] = Field("asc", description="Sort direction (asc or desc)")
    
    @property
    def page(self) -> int:
        """Calculate current page number (1-indexed)."""
        return (self.skip // self.limit) + 1
    
    def to_page_response(self, total: int) -> Dict[str, Any]:
        """Generate pagination metadata for response.
        
        Args:
            total: Total number of records
            
        Returns:
            Dictionary with pagination metadata
        """
        pages = (total + self.limit - 1) // self.limit if self.limit > 0 else 0
        return {
            "total": total,
            "page": self.page,
            "size": self.limit,
            "pages": pages,
            "sort_field": self.sort_field,
            "sort_direction": self.sort_direction
        }


class ExportFormat(str, Enum):
    """Supported export formats."""
    
    CSV = "csv"
    VOTABLE = "votable"
    # FITS = "fits"  # Future implementation


class ExportOptions(BaseSchema):
    """Options for exporting data."""
    
    format: ExportFormat = Field(
        default=ExportFormat.CSV, 
        description="Format to export the data in"
    )
    selected_fields: Optional[List[str]] = Field(
        default=None, 
        description="List of fields to include in the export. If not provided, all fields will be included."
    )
    include_metadata: bool = Field(
        default=True, 
        description="Whether to include metadata in the export file."
    ) 