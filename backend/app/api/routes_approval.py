from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.services.approval_service import ApprovalService
from app.schemas.approval import ApprovalOut, ApprovalAction

router = APIRouter(prefix="/approvals", tags=["Approvals"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{employee_id}", response_model=list[ApprovalOut])
def get_pending_approvals(employee_id: int, db: Session = Depends(get_db)):
    service = ApprovalService(db)
    return service.get_pending_for_employee(employee_id)

@router.post("/{approval_id}/action", response_model=ApprovalOut)
def update_approval_status(approval_id: int, action: ApprovalAction, db: Session = Depends(get_db)):
    service = ApprovalService(db)
    updated = service.process_approval(approval_id, action.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Approval not found")
    return updated