from sqlalchemy.orm import Session
from app.repos.visitor_repo import VisitorRepository
from typing import Optional
from app.utils.image_uploader import upload_image_base64
from app.services.approval_service import ApprovalService

class VisitorService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = VisitorRepository(db)
    
    def register_visitor(self, data: dict):
        photo_url = None
        if data.get("photo_base64"):
            photo_url = upload_image_base64(data["photo_base64"])

        visitor_data = {
            "full_name": data["full_name"],
            "contact": data["contact"],
            "company": data.get("company"),
            "purpose": data["purpose"],
            "host_employee_name": data["host_employee_name"],
            "host_department": data["host_department"],
            "photo_url": photo_url,
        }

        visitor = self.repo.create_visitor(visitor_data)

        approval_service = ApprovalService(self.db)
        approval_service.create_approval_request(visitor.id, employee_id=1)
        
        return visitor
    
    def fetch_visitor(self, visitor_id: int):
        return self.repo.get_visitor_by_id(visitor_id)