from sqlalchemy.orm import Session
from app.models import Visitor

class VisitorRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_visitor(self, visitor_data: dict) -> Visitor:
        visitor = Visitor(**visitor_data)
        self.db.add(visitor)
        self.db.commit()
        self.db.refresh(visitor)
        return visitor
    
    def get_visitor_by_id(self, visitor_id: int) -> Visitor | None:
        return self.db.query(Visitor).filter(Visitor.id == visitor_id).first()