from sqlalchemy.orm import Session
from app.repos.approval_repo import ApprovalRepository
from app.models import ApprovalStatus

class ApprovalService:
    def __init__(self, db: Session):
        self.repo = ApprovalRepository(db)
    
    def create_approval_request(self, visitor_id: int, employee_id: int):
        return self.repo.create_approval(visitor_id, employee_id)
    
    def get_pending_for_employee(self, employee_id: int):
        return self.repo.get_pending_approvals_for_employee(employee_id)
    
    def process_approval(self, approval_id: int, status: str):
        if status not in ApprovalStatus.__members__:
            raise ValueError("Invalid approval status")
        return self.repo.update_status(approval_id, ApprovalStatus[status])