from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Base, engine
import app.models
from app.api.routes_visitor import router as visitor_router
from app.api.routes_approval import router as approval_router
from app.api.routes_preapproval import router as preapproval_router
app = FastAPI()

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

@app.get("/")
def root():
    return {"message": "Visitor management API is live"}