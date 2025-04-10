from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from services.sed_service import SEDService
from schemas.sed import SEDRequest, SEDResponse

router = APIRouter(prefix="/sed", tags=["sed"])

def get_sed_service() -> SEDService:
    """Dependency injection for SED service."""
    return SEDService()

@router.post("/process", response_model=SEDResponse)
async def process_sed(
    request: SEDRequest,
    sed_service: SEDService = Depends(get_sed_service)
) -> SEDResponse:
    """
    Process SED data and generate visualization.
    
    Args:
        request: SED processing request containing raw data
        sed_service: Injected SED service
        
    Returns:
        SEDResponse with processing status and SED name
    """
    try:
        sed_name, _ = await sed_service.process_sed(request.raw_data)
        return SEDResponse(
            sed_name=sed_name,
            status="success",
            message="SED processed successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/download/{sed_name}")
async def download_sed(
    sed_name: str,
    sed_service: SEDService = Depends(get_sed_service)
) -> FileResponse:
    """
    Download a generated SED image.
    
    Args:
        sed_name: Name of the SED to download
        sed_service: Injected SED service
        
    Returns:
        FileResponse with the SED image
        
    Raises:
        HTTPException: If SED file not found
    """
    file_path = await sed_service.get_sed_file(sed_name)
    if not file_path:
        raise HTTPException(
            status_code=404,
            detail=f"SED '{sed_name}' not found"
        )
    
    return FileResponse(
        str(file_path),
        media_type="image/png",
        filename=f"{sed_name}.png"
    ) 