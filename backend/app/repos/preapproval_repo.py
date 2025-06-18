from sqlalchemy.orm import Session
from app.models import PreApproval

class PreApprovalRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_preapproval(self, visitor_id: int, employee_id: int, valid_from, valid_to, max_visits_per_day: int = 5):
        pa = PreApproval(
            visitor_id=visitor_id,
            employee_id=employee_id,
            valid_from=valid_from,
            valid_to=valid_to,
            max_visits_per_day=max_visits_per_day
        )
        self.db.add(pa)
        self.db.commit()
        self.db.refresh(pa)
        return pa
    
    def get_preapprovals_for_employee(self, employee_id: int):
        return (
            self.db.query(PreApproval)
            .filter(PreApproval.employee_id == employee_id)
            .all()
        )