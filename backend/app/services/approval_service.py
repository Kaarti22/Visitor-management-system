from sqlalchemy.orm import Session
from app.repos.approval_repo import ApprovalRepository
from app.repos.visitor_repo import VisitorRepository
from app.utils.qr_generator import generate_qr_and_upload
from app.models import ApprovalStatus

class ApprovalService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ApprovalRepository(db)
    
    def create_approval_request(self, visitor_id: int, employee_id: int):
        return self.repo.create_approval(visitor_id, employee_id)
    
    def get_pending_for_employee(self, employee_id: int):
        return self.repo.get_pending_approvals_for_employee(employee_id)
    
    def process_approval(self, approval_id: int, status: str):
        if status not in ApprovalStatus.__members__:
            raise ValueError("Invalid approval status")
        
        updated = self.repo.update_status(approval_id, ApprovalStatus[status])

        if updated and status == "APPROVED":
            qr_data = f"visitor:{updated.visitor_id}"
            badge_url = generate_qr_and_upload(qr_data, filename=f"badge_{updated.visitor_id}")

            visitor_repo = VisitorRepository(self.db)
            visitor = visitor_repo.get_visitor_by_id(updated.visitor_id)
            if visitor:
                visitor.badge_url = badge_url
                self.db.commit()

        return updated