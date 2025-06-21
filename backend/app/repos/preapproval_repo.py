"""
repos/preapproval_repo.py — Repository for managing pre-approval data operations.
"""

from sqlalchemy.orm import Session
from app.models import PreApproval


class PreApprovalRepository:
    """
    Handles database interactions related to pre-approvals.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_preapproval(
        self,
        visitor_id: int,
        employee_id: int,
        valid_from,
        valid_to,
        max_visits_per_day: int = 5
    ) -> PreApproval:
        """
        Creates a new pre-approval record in the database.

        Args:
            visitor_id (int): ID of the visitor.
            employee_id (int): ID of the approving employee.
            valid_from (datetime): Start of the allowed visit window.
            valid_to (datetime): End of the allowed visit window.
            max_visits_per_day (int, optional): Limit for visits per day. Defaults to 5.

        Returns:
            PreApproval: The created pre-approval record.
        """
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

    def get_preapprovals_for_employee(self, employee_id: int) -> list[PreApproval]:
        """
        Retrieves all pre-approvals scheduled by a specific employee.

        Args:
            employee_id (int): Employee ID.

        Returns:
            list[PreApproval]: List of pre-approval records.
        """
        return (
            self.db.query(PreApproval)
            .filter(PreApproval.employee_id == employee_id)
            .all()
        )
