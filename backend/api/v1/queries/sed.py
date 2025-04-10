from fastapi import APIRouter, HTTPException, Response
from schemas.sed import SEDRequest, SEDResponse
from services.sed_service import SEDService

router = APIRouter(prefix="/sed", tags=["sed"])

@router.post("/process", response_model=SEDResponse)
async def process_sed(request: SEDRequest) -> SEDResponse:
    """Process SED data and generate visualization."""
    try:
        sed_service = SEDService()
        sed_name, _ = await sed_service.process_sed(request.raw_data)
        return SEDResponse(
            sed_name=sed_name,
            status="success",
            message="SED processed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{sed_name}")
async def download_sed(sed_name: str) -> Response:
    """Download generated SED visualization."""
    try:
        sed_service = SEDService()
        file_path = await sed_service.get_sed_file(sed_name)
        if not file_path:
            raise HTTPException(status_code=404, detail="SED file not found")
            
        return Response(
            content=file_path.read_bytes(),
            media_type="image/png"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 