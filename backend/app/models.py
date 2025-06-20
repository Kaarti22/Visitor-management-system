from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
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

    approvals = relationship("Approval", back_populates="visitor")

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class PreApproval(Base):
    __tablename__ = "preapprovals"

    id = Column(Integer, primary_key=True, index=True)

    visitor_id = Column(Integer, ForeignKey("visitors.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    valid_from = Column(DateTime(timezone=True), nullable=False)
    valid_to = Column(DateTime(timezone=True), nullable=False)

    max_visits_per_day = Column(Integer, default=5)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=False)

    visitor_id = Column(Integer, ForeignKey("visitors.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    status = Column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING, nullable=False)

    requested_at = Column(DateTime(timezone=True), server_default=func.now())
    decision_at = Column(DateTime(timezone=True), nullable=True)

    visitor = relationship("Visitor", back_populates="approvals")