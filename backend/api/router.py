from fastapi import APIRouter

from .v1 import router as v1_router
from core.config import settings

# Main router that includes versioned sub-routers
router = APIRouter()

# Include API v1 routes with prefix
router.include_router(
    v1_router,
    prefix=settings.API_V1_STR,
) 