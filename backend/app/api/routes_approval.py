"""
api/routes_approval.py — API endpoints for handling visitor approval workflows.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from app.core.config import SessionLocal
from app.services.approval_service import ApprovalService
from app.schemas.approval import ApprovalOut, ApprovalAction
from app.models import Approval
from typing import Optional, Generator

router = APIRouter(prefix="/approvals", tags=["Approvals"])

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to provide a SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{employee_id}", response_model=list[ApprovalOut])
def get_approvals(
    employee_id: int,
    status: Optional[str] = Query(None, description="Filter approvals by status"),
    db: Session = Depends(get_db)
):
    """
    Get all approval requests for a specific employee.
    - Optional filter: status (e.g., PENDING, APPROVED, REJECTED)
    """
    query = db.query(Approval).options(joinedload(Approval.visitor)).filter(Approval.employee_id == employee_id)

    if status:
        query = query.filter(Approval.status == status.upper())

    return query.all()


@router.post("/{approval_id}/action", response_model=ApprovalOut)
def update_approval_status(
    approval_id: int,
    action: ApprovalAction,
    db: Session = Depends(get_db)
):
    """
    Update the status of an approval request (approve or reject).
    - Changes status and records decision timestamp.
    """
    service = ApprovalService(db)
    updated = service.process_approval(approval_id, action.status)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval not found"
        )

    return updated
