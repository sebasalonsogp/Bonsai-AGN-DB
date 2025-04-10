from pydantic import BaseModel, Field
from typing import Optional

class SEDRequest(BaseModel):
    """Schema for SED processing request."""
    raw_data: str = Field(
        ...,
        description="Space-separated wavelength,flux pairs (e.g., '1000,1.2 2000,1.5 3000,1.8')"
    )

class SEDResponse(BaseModel):
    """Schema for SED processing response."""
    sed_name: str = Field(..., description="Unique identifier for the generated SED")
    status: str = Field(..., description="Processing status")
    message: Optional[str] = Field(None, description="Additional information about the processing") 