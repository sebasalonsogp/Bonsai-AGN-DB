import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.config import settings
from core.logging_config import setup_logging
from core.exceptions import register_exception_handlers
from api import router as api_router
from database import Base, engine


# Set up logging using Loguru with custom configuration
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events for application startup and shutdown.
    
    This async context manager handles initialization tasks before the application
    starts serving requests and cleanup tasks when the application is shutting down.
    It is used with FastAPI's lifespan parameter to manage application lifecycle.
    
    Args:
        app: FastAPI application instance
    """
    # Startup: Create tables if they don't exist (commented out for production use)
    logger.info("Starting AGN-DB API")
    # Uncomment the next line to create tables automatically - for development only
    # This is disabled by default as migrations should handle schema changes in production
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    
    # Yield control to the application - FastAPI will serve requests
    yield
    
    # Shutdown: Clean up resources, close connections, etc.
    logger.info("Shutting down AGN-DB API")
    # Add any cleanup operations here (e.g., close connections, stop background tasks)


# Create FastAPI application with metadata and lifecycle management
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# Register global exception handlers for consistent error responses
register_exception_handlers(app)

# Configure CORS to allow frontend applications to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router with all routes from the api module
# This includes all version-specific endpoints under /api/v{version}/
app.include_router(api_router)


@app.get("/")
async def root():
    """
    Root endpoint for health check and API information.
    
    Provides basic information about the API service, including
    its name, version, and current status. This endpoint can be used
    by monitoring tools to verify the service is running.
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health():
    """
    Health check endpoint for monitoring systems.
    
    Returns a simple status indicator that can be used by load balancers,
    container orchestrators, or monitoring tools to verify the service
    is responsive and healthy.
    """
    return {"status": "healthy"} 