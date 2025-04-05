from fastapi import APIRouter

# Import command routers here as they are implemented
from .sources import router as sources_router 
from .photometry import router as photometry_router
from .redshift import router as redshift_router
from .classification import router as classification_router

# Create commands router to aggregate all command endpoints
router = APIRouter(tags=["Commands"])

# Include specific command routers here as they are implemented
router.include_router(sources_router)
router.include_router(photometry_router)
router.include_router(redshift_router)
router.include_router(classification_router)

__all__ = ["router"] 