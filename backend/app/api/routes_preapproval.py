from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.preapproval import PreApprovalCreate, PreApprovalOut
from app.services.preapproval_service import PreApprovalService

router = APIRouter(prefix="/preapprovals", tags=["PreApprovals"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PreApprovalOut, status_code=status.HTTP_201_CREATED)
def create_preapproval(data: PreApprovalCreate, db: Session = Depends(get_db)):
    service = PreApprovalService(db)
    pa = service.schedule_visit(**data.dict())
    return pa

@router.get("/{employee_id}", response_model=list[PreApprovalOut])
def list_preapprovals(employee_id: int, db: Session = Depends(get_db)):
    service = PreApprovalService(db)
    return service.list_preapprovals(employee_id)