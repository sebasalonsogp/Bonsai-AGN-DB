from fastapi import APIRouter

# Import query routers here as they are implemented
from .sources import router as sources_router
from .photometry import router as photometry_router
from .redshift import router as redshift_router
from .classification import router as classification_router
from .search import router as search_router
from .sed import router as sed_router

# Create queries router to aggregate all query endpoints
router = APIRouter(prefix="/queries", tags=["queries"])

# Include specific query routers here as they are implemented
router.include_router(sources_router)
router.include_router(photometry_router)
router.include_router(redshift_router)
router.include_router(classification_router)
router.include_router(search_router)
router.include_router(sed_router)

__all__ = ["router"] 