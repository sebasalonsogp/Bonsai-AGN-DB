from fastapi import APIRouter, HTTPException, Response
from schemas.sed import SEDRequest, SEDResponse
from services.sed_service import SEDService
from loguru import logger

router = APIRouter(prefix="/sed", tags=["sed"])

@router.post("/process", response_model=SEDResponse)
async def process_sed(request: SEDRequest) -> SEDResponse:
    """Process SED data and generate visualization."""
    try:
        logger.info("Received SED processing request")
        logger.info(f"Request data length: {len(request.raw_data)}")
        logger.info(f"First 100 characters of data: {request.raw_data[:100]}")
        
        sed_service = SEDService()
        sed_name, _ = await sed_service.process_sed(request.raw_data)
        logger.info(f"SED processed successfully, generated file: {sed_name}")
        
        return SEDResponse(
            sed_name=sed_name,
            status="success",
            message="SED processed successfully"
        )
    except Exception as e:
        logger.error(f"Error in SED processing endpoint: {str(e)}")
        logger.error(f"Error occurred with data length: {len(request.raw_data)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{sed_name}")
async def download_sed(sed_name: str) -> Response:
    """Download generated SED visualization."""
    try:
        logger.info(f"Received SED download request for: {sed_name}")
        logger.info(f"Request URL: /api/v1/queries/sed/download/{sed_name}")
        sed_service = SEDService()
        file_path = await sed_service.get_sed_file(sed_name)
        logger.info(f"Service returned file path: {file_path}")
        
        if not file_path:
            logger.error(f"SED file not found: {sed_name}")
            logger.error(f"Expected file path: {sed_service.sed_output_dir / f'{sed_name}.png'}")
            raise HTTPException(status_code=404, detail="SED file not found")
            
        logger.info(f"Attempting to read file: {file_path}")
        file_content = file_path.read_bytes()
        logger.info(f"Successfully read {len(file_content)} bytes from file")
        
        return Response(
            content=file_content,
            media_type="image/png"
        )
    except Exception as e:
        logger.error(f"Error in SED download endpoint: {str(e)}")
        logger.error(f"Error occurred with sed_name: {sed_name}")
        logger.error(f"Error occurred with file_path: {file_path}")
        raise HTTPException(status_code=500, detail=str(e)) 