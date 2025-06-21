"""
repos/approval_repo.py — Repository layer for Approval operations (CRUD & status updates).
"""

from sqlalchemy.orm import Session
from app.models import Approval, ApprovalStatus
from datetime import datetime


class ApprovalRepository:
    """
    Repository class for managing approvals in the database.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_approval(self, visitor_id: int, employee_id: int) -> Approval:
        """
        Creates a new approval request with default status = PENDING.
        """
        approval = Approval(visitor_id=visitor_id, employee_id=employee_id)
        self.db.add(approval)
        self.db.commit()
        self.db.refresh(approval)
        return approval

    def get_pending_approvals_for_employee(self, employee_id: int):
        """
        Retrieves all pending approval requests assigned to a specific employee.
        """
        return self.db.query(Approval).filter(
            Approval.employee_id == employee_id,
            Approval.status == ApprovalStatus.PENDING
        ).all()

    def update_status(self, approval_id: int, status: ApprovalStatus):
        """
        Updates the status of an approval request (APPROVED or REJECTED).
        Automatically sets decision time for terminal states.
        """
        approval = self.db.query(Approval).filter(Approval.id == approval_id).first()
        if approval:
            approval.status = status
            if status in [ApprovalStatus.APPROVED, ApprovalStatus.REJECTED]:
                approval.decision_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(approval)
        return approval
