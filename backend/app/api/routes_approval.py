from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.services.approval_service import ApprovalService
from app.schemas.approval import ApprovalOut, ApprovalAction
from app.models import Approval
from typing import Optional, List

router = APIRouter(prefix="/approvals", tags=["Approvals"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{employee_id}", response_model=list[ApprovalOut])
def get_approvals(
    employee_id: int, 
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Approval).filter(Approval.employee_id == employee_id)
    if status:
        query = query.filter(Approval.status == status.upper())
    return query.all()

@router.post("/{approval_id}/action", response_model=ApprovalOut)
def update_approval_status(approval_id: int, action: ApprovalAction, db: Session = Depends(get_db)):
    service = ApprovalService(db)
    updated = service.process_approval(approval_id, action.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Approval not found")
    return updated