from fastapi import APIRouter

from .commands import router as commands_router
from .queries import router as queries_router

# Main v1 router that combines commands and queries
router = APIRouter()

# Include commands and queries routers
router.include_router(commands_router)
router.include_router(queries_router)

__all__ = ["router"] 