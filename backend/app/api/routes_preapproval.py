from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.preapproval import PreApprovalCreate, PreApprovalOut
from app.services.preapproval_service import PreApprovalService
from app.dependencies.auth_dep import get_current_user
from app.models import Visitor, Employee

router = APIRouter(prefix="/preapprovals", tags=["PreApprovals"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PreApprovalOut, status_code=status.HTTP_201_CREATED)
def create_preapproval(
    data: PreApprovalCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if data.employee_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized preapproval attempt")
    
    visitor = db.query(Visitor).filter_by(id=data.visitor_id).first()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    
    employee = db.query(Employee).get(current_user["id"])

    if visitor.host_employee_name.strip().lower() != employee.name.strip().lower():
        raise HTTPException(status_code=403, detail="Only the assigned host can pre-approve this visitor.")

    service = PreApprovalService(db)
    pa = service.schedule_visit(**data.dict())
    return pa

@router.get("/{employee_id}", response_model=list[PreApprovalOut])
def list_preapprovals(employee_id: int, db: Session = Depends(get_db)):
    service = PreApprovalService(db)
    return service.list_preapprovals(employee_id)