from sqlalchemy.orm import Session
from app.repos.preapproval_repo import PreApprovalRepository

class PreApprovalService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PreApprovalRepository(db)
    
    def schedule_visit(self, visitor_id: int, employee_id: int, valid_from, valid_to, max_visits_per_day: int = 5):
        return self.repo.create_preapproval(visitor_id, employee_id, valid_from, valid_to, max_visits_per_day)
    
    def list_preapprovals(self, employee_id: int):
        return self.repo.get_preapprovals_for_employee(employee_id)