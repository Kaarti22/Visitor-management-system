"""
services/visitor_service.py — Handles visitor registration and data retrieval.
"""

from sqlalchemy.orm import Session
from app.repos.visitor_repo import VisitorRepository
from app.repos.employee_repo import EmployeeRepository
from app.services.approval_service import ApprovalService
from app.utils.image_uploader import upload_image_base64
from app.logger_config import setup_logger

logger = setup_logger()

class VisitorService:
    """
    Manages business logic for visitor-related operations:
    - Registration
    - Lookup
    """

    def __init__(self, db: Session):
        self.db = db
        self.repo = VisitorRepository(db)

    def register_visitor(self, data: dict):
        """
        Registers a new visitor, uploads photo, stores info, and sends approval request.

        Args:
            data (dict): Visitor details from the request body.

        Returns:
            Visitor: The created visitor instance.
        
        Raises:
            Exception: If host employee is not found.
        """
        logger.info(f"📝 Registering visitor: {data.get('full_name')}")

        # Upload photo if provided
        photo_url = None
        if data.get("photo_base64"):
            logger.info("📷 Uploading visitor photo...")
            photo_url = upload_image_base64(data["photo_base64"])

        # Build visitor data dict
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
        logger.info(f"✅ Visitor record created with ID {visitor.id}")

        # Fetch host employee
        employee_repo = EmployeeRepository(self.db)
        host = employee_repo.get_employee_by_name(data["host_employee_name"])

        if not host:
            logger.error("❌ Host employee not found")
            raise Exception("Host employee not found")

        # Create approval request
        logger.info(f"🔔 Creating approval request for host ID {host.id}")
        approval_service = ApprovalService(self.db)
        approval_service.create_approval_request(visitor.id, employee_id=host.id)

        return visitor

    def fetch_visitor(self, visitor_id: int):
        """
        Fetches visitor details by ID.

        Args:
            visitor_id (int): The ID of the visitor to fetch.

        Returns:
            Visitor | None: Visitor object or None if not found.
        """
        logger.info(f"🔎 Fetching visitor with ID {visitor_id}")
        return self.repo.get_visitor_by_id(visitor_id)
