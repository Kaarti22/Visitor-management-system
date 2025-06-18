from sqlalchemy.orm import Session
from app.models import Employee

class EmployeeRespository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_employee_by_name(self, name: str):
        return self.db.query(Employee).filter(Employee.name == name).first()