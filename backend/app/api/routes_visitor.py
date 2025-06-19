from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.visitor import VisitorCreate, VisitorOut
from app.services.visitor_service import VisitorService
from app.core.config import SessionLocal

router = APIRouter(prefix="/visitors", tags=["Visitors"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{visitor_id}", response_model=VisitorOut)
def get_visitor(visitor_id: int, db: Session = Depends(get_db)):
    service = VisitorService(db)
    visitor = service.fetch_visitor(visitor_id)
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return visitor

@router.post("/register", response_model=VisitorOut, status_code=status.HTTP_201_CREATED)
def register_visitor(data: VisitorCreate, db: Session = Depends(get_db)):
    service = VisitorService(db)
    visitor = service.register_visitor(data.dict())
    return visitor