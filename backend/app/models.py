from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .core.config import Base

class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=False)
    full_name = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    company = Column(String)
    purpose = Column(String, nullable=False)
    host_employee_name = Column(String, nullable=False)
    host_department = Column(String, nullable=False)
    photo_url = Column(String)
    badge_url = Column(String)
    check_in = Column(DateTime(timezone=True), server_default=func.now())
    check_out = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
