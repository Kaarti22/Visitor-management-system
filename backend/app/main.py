from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
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

logger = setup_logger()

app = FastAPI()
logger.info("Server started")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(visitor_router)
app.include_router(approval_router)
app.include_router(preapproval_router)
app.include_router(employee_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Visitor management API is live"}

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occured. Please try again."}
    )

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTP Exception: {exc.detail}")
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )