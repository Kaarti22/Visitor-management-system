"""
repos/employee_repo.py — Repository layer for querying employee records.
"""

from sqlalchemy.orm import Session
from app.models import Employee


class EmployeeRepository:
    """
    Repository class to manage employee data operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_employee_by_name(self, name: str) -> Employee | None:
        """
        Retrieves an employee record by their exact name.

        Args:
            name (str): Full name of the employee.

        Returns:
            Employee | None: Employee object if found, otherwise None.
        """
        return self.db.query(Employee).filter(Employee.name == name).first()
