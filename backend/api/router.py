from fastapi import APIRouter
from api.v1.queries import sources, photometry, redshift, classification, search, sed
from api.v1.commands import sources as cmd_sources, photometry as cmd_photometry, redshift as cmd_redshift, classification as cmd_classification

# Create main router
router = APIRouter()

# Include version 1 routers
router.include_router(sources.router, prefix="/api/v1/queries/sources", tags=["sources"])
router.include_router(photometry.router, prefix="/api/v1/queries/photometry", tags=["photometry"])
router.include_router(redshift.router, prefix="/api/v1/queries/redshift", tags=["redshift"])
router.include_router(classification.router, prefix="/api/v1/queries/classification", tags=["classification"])
router.include_router(search.router, prefix="/api/v1/queries/search", tags=["search"])
router.include_router(sed.router, prefix="/api/v1/queries/sed", tags=["sed"])

# Include version 1 command routers
router.include_router(cmd_sources.router, prefix="/api/v1/commands/sources", tags=["sources"])
router.include_router(cmd_photometry.router, prefix="/api/v1/commands/photometry", tags=["photometry"])
router.include_router(cmd_redshift.router, prefix="/api/v1/commands/redshift", tags=["redshift"])
router.include_router(cmd_classification.router, prefix="/api/v1/commands/classification", tags=["classification"]) 