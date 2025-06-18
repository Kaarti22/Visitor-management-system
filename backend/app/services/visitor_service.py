from sqlalchemy.orm import Session
from app.repos.visitor_repo import VisitorRepository
from typing import Optional

class VisitorService:
    def __init__(self, db: Session):
        self.repo = VisitorRepository(db)
    
    def register_visitor(self, data: dict):
        # TODO: Add Cloudinary photo upload and validations
        visitor = self.repo.create_visitor(data)
        return visitor
    
    def fetch_visitor(self, visitor_id: int):
        return self.repo.get_visitor_by_id(visitor_id)