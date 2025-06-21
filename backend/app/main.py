"""
main.py - Entry point of the FastAPI Visitor Management System.

Initializes:
- FastAPI app
- Routers for visitors, approvals, pre-approvals, employees, and auth
- Global CORS config
- Exception handling with logging
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import Base, engine
from app.api.routes_visitor import router as visitor_router
from app.api.routes_approval import router as approval_router
from app.api.routes_preapproval import router as preapproval_router
from app.api.routes_employee import router as employee_router
from app.api.routes_auth import router as auth_router
from app.logger_config import setup_logger
from fastapi.encoders import jsonable_encoder

# Initialize app and logger
app = FastAPI()
logger = setup_logger()
logger.info("✅ FastAPI server started")

# CORS Middleware Configuration (open for all origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables based on SQLAlchemy models
Base.metadata.create_all(bind=engine)
logger.info("✅ Database tables ensured via SQLAlchemy")

# Register route modules
app.include_router(visitor_router)
app.include_router(approval_router)
app.include_router(preapproval_router)
app.include_router(employee_router)
app.include_router(auth_router)

@app.get("/")
def root():
    """Health check route."""
    logger.info("⚙️  Root endpoint accessed.")
    return {"message": "Visitor management API is live"}

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Global fallback for unhandled exceptions.
    Logs the traceback and returns a generic 500 error.
    """
    logger.error(f"❌ Unhandled error occurred during {request.method} {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again."}
    )

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handles HTTPExceptions (like 404, 403).
    """
    logger.warning(f"⚠️ HTTP Exception during {request.method} {request.url}: {exc.detail}")
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles Pydantic validation errors in request bodies, query params, etc.
    """
    logger.warning(f"⚠️ Validation error during {request.method} {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": jsonable_encoder(exc.errors())}
    )
