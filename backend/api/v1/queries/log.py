from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from loguru import logger

router = APIRouter()

class LogRequest(BaseModel):
    action: str
    timestamp: str
    has_queries: bool
    modal_state: bool

@router.post("/log")
async def log_action(request: LogRequest):
    """Log frontend actions for debugging purposes."""
    try:
        logger.info(f"Frontend action: {request.action}")
        logger.info(f"Timestamp: {request.timestamp}")
        logger.info(f"Has queries: {request.has_queries}")
        logger.info(f"Modal state: {request.modal_state}")
        return {"status": "logged"}
    except Exception as e:
        logger.error(f"Error logging action: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 