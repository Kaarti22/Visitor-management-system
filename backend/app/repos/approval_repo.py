from sqlalchemy.orm import Session
from app.models import Approval, ApprovalStatus

class ApprovalRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_approval(self, visitor_id: int, employee_id: int) -> Approval:
        approval = Approval(visitor_id=visitor_id, employee_id=employee_id)
        self.db.add(approval)
        self.db.commit()
        self.db.refresh(approval)
        return approval
    
    def get_pending_approvals_for_employee(self, employee_id: int):
        return self.db.query(Approval).filter(
            Approval.employee_id == employee_id,
            Approval.status == ApprovalStatus.PENDING
        ).all()
    
    def update_status(self, approval_id: int, status: ApprovalStatus):
        approval = self.db.query(Approval).filter(Approval.id == approval_id).first()
        if approval:
            approval.status = status
            self.db.commit()
            self.db.refresh(approval)
        return approval