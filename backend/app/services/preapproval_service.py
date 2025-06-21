"""
services/preapproval_service.py — Handles business logic for scheduling and retrieving pre-approvals.
"""

from sqlalchemy.orm import Session
from datetime import datetime
from app.repos.preapproval_repo import PreApprovalRepository
from app.logger_config import setup_logger

logger = setup_logger()

class PreApprovalService:
    """
    Manages pre-approval logic, including scheduling and retrieving pre-approved visit windows.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repo = PreApprovalRepository(db)

    def schedule_visit(
        self,
        visitor_id: int,
        employee_id: int,
        valid_from: datetime,
        valid_to: datetime,
        max_visits_per_day: int = 5
    ):
        """
        Schedules a pre-approved visit for a visitor.

        Args:
            visitor_id (int): ID of the visitor.
            employee_id (int): ID of the employee scheduling the visit.
            valid_from (datetime): Start of the valid window.
            valid_to (datetime): End of the valid window.
            max_visits_per_day (int): Max allowed visits per day. Default is 5.

        Returns:
            PreApproval: The created pre-approval entry.
        """
        logger.info(
            f"📅 Scheduling pre-approval: visitor={visitor_id}, employee={employee_id}, "
            f"from={valid_from}, to={valid_to}, max/day={max_visits_per_day}"
        )
        return self.repo.create_preapproval(
            visitor_id=visitor_id,
            employee_id=employee_id,
            valid_from=valid_from,
            valid_to=valid_to,
            max_visits_per_day=max_visits_per_day
        )

    def list_preapprovals(self, employee_id: int):
        """
        Lists all pre-approvals scheduled by a given employee.

        Args:
            employee_id (int): ID of the employee.

        Returns:
            List[PreApproval]: List of pre-approval entries.
        """
        logger.info(f"📋 Fetching pre-approvals for employee {employee_id}")
        return self.repo.get_preapprovals_for_employee(employee_id)
