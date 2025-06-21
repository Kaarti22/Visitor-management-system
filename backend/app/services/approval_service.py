"""
services/approval_service.py — Contains business logic for handling visitor approvals.
"""

from sqlalchemy.orm import Session
from app.repos.approval_repo import ApprovalRepository
from app.repos.visitor_repo import VisitorRepository
from app.utils.qr_generator import generate_qr_and_upload
from app.models import ApprovalStatus
from app.logger_config import setup_logger

logger = setup_logger()

class ApprovalService:
    """
    Handles core approval workflows:
    - Creating requests
    - Processing decisions
    - Generating QR badges for approved visitors
    """

    def __init__(self, db: Session):
        self.db = db
        self.repo = ApprovalRepository(db)

    def create_approval_request(self, visitor_id: int, employee_id: int):
        """
        Creates a new approval request for a visitor.

        Args:
            visitor_id (int): ID of the visitor.
            employee_id (int): ID of the host employee.

        Returns:
            Approval: The created approval record.
        """
        logger.info(f"🔄 Creating approval request for visitor {visitor_id} and employee {employee_id}")
        return self.repo.create_approval(visitor_id, employee_id)

    def get_pending_for_employee(self, employee_id: int):
        """
        Fetches all pending approval requests for a given employee.

        Args:
            employee_id (int): ID of the employee.

        Returns:
            List[Approval]: List of pending approvals.
        """
        logger.info(f"📥 Fetching pending approvals for employee {employee_id}")
        return self.repo.get_pending_approvals_for_employee(employee_id)

    def process_approval(self, approval_id: int, status: str):
        """
        Updates the approval status and generates a badge if approved.

        Args:
            approval_id (int): ID of the approval to update.
            status (str): New status ('APPROVED', 'REJECTED').

        Returns:
            Approval | None: The updated approval object or None if failed.
        """
        if status not in ApprovalStatus.__members__:
            logger.warning(f"❌ Invalid approval status received: {status}")
            raise ValueError("Invalid approval status")

        logger.info(f"⚙️ Processing approval ID {approval_id} with status {status}")
        updated = self.repo.update_status(approval_id, ApprovalStatus[status])

        # If approval successful and status is APPROVED, generate QR badge
        if updated and status == "APPROVED":
            qr_data = f"visitor:{updated.visitor_id}"
            badge_url = generate_qr_and_upload(qr_data, filename=f"badge_{updated.visitor_id}")

            if not badge_url:
                logger.warning(f"⚠️ QR badge generation failed for visitor {updated.visitor_id}")

            visitor_repo = VisitorRepository(self.db)
            visitor = visitor_repo.get_visitor_by_id(updated.visitor_id)

            if visitor:
                visitor.badge_url = badge_url
                self.db.commit()
                logger.info(f"✅ Badge URL saved for visitor {visitor.id}")
            else:
                logger.error(f"❌ Visitor {updated.visitor_id} not found while saving badge")

        return updated
