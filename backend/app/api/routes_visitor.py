from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.visitor import VisitorCreate, VisitorOut
from app.services.visitor_service import VisitorService
from app.core.config import SessionLocal
from app.models import Employee
from datetime import datetime

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
    host = (
        db.query(Employee)
        .filter(
            Employee.name.ilike(data.host_employee_name.strip()),
            Employee.department.ilike(data.host_department.strip())
        )
        .first()
    )
    if not host:
        raise HTTPException(
            status_code=400,
            detail="Host employee not found in the specified department"
        )

    service = VisitorService(db)
    visitor = service.register_visitor(data.dict())
    return visitor

@router.patch("/{visitor_id}/checkout", response_model=VisitorOut)
def checkout_visitor(visitor_id: int, db: Session = Depends(get_db)):
    service = VisitorService(db)
    visitor = service.fetch_visitor(visitor_id)

    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    
    if visitor.check_out:
        raise HTTPException(status_code=400, detail="Visitor already checkout out")
    
    visitor.check_out = datetime.utcnow()
    db.commit()
    db.refresh(visitor)

    return visitor