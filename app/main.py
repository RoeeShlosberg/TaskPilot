from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging
from app.core.config import settings
from app.db.session import create_db_and_tables
from app.api import tasks, agent


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)


# Global exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()} at {request.url}")
    return JSONResponse(
        status_code=400,
        content={"detail": f"Bad request: {exc.errors()}"}
    )


@app.on_event("startup")
def on_startup():
    """
    Initialize database tables on app startup
    """
    create_db_and_tables()


# Include API routes
app.include_router(tasks.router, prefix=settings.api_v1_prefix)
app.include_router(agent.router, prefix=settings.api_v1_prefix)


@app.get("/")
def root():
    """
    Root endpoint
    """
    return {"message": f"Welcome to {settings.app_name}"}


@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "app": settings.app_name, "version": settings.app_version}
