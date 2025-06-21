"""
models.py — SQLAlchemy ORM models for the Visitor Management System.

Defines:
- Visitor: Individual visiting the premises
- Employee: Host employee for the visitor
- Approval: Manual/automatic approval records
- PreApproval: Scheduled advance approvals
- ApprovalStatus: Enum for visitor approval state
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .core.config import Base
import enum

# -----------------------
# Enums
# -----------------------

class ApprovalStatus(str, enum.Enum):
    """Defines possible approval statuses for a visitor."""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

# -----------------------
# Visitor Model
# -----------------------

class Visitor(Base):
    """Represents a visitor record including identity, purpose, and timestamps."""
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    company = Column(String)
    purpose = Column(String, nullable=False)
    host_employee_name = Column(String, nullable=False)
    host_department = Column(String, nullable=False)
    
    photo_url = Column(String)           # Cloudinary-hosted photo
    badge_url = Column(String)           # Cloudinary-hosted QR badge

    check_in = Column(DateTime(timezone=True), server_default=func.now())
    check_out = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    approvals = relationship("Approval", back_populates="visitor")

# -----------------------
# Employee Model
# -----------------------

class Employee(Base):
    """Represents a host employee responsible for approving visitor entries."""
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)  # Hashed password
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# -----------------------
# Approval Model
# -----------------------

class Approval(Base):
    """Stores each approval action, including status and timestamps."""
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True)

    visitor_id = Column(Integer, ForeignKey("visitors.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    status = Column(Enum(ApprovalStatus), nullable=False, default=ApprovalStatus.PENDING)

    requested_at = Column(DateTime(timezone=True), server_default=func.now())
    decision_at = Column(DateTime(timezone=True), nullable=True)

    visitor = relationship("Visitor", back_populates="approvals")

# -----------------------
# Pre-Approval Model
# -----------------------

class PreApproval(Base):
    """Defines a scheduled time window during which a visitor is pre-approved."""
    __tablename__ = "preapprovals"

    id = Column(Integer, primary_key=True, index=True)

    visitor_id = Column(Integer, ForeignKey("visitors.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    valid_from = Column(DateTime(timezone=True), nullable=False)
    valid_to = Column(DateTime(timezone=True), nullable=False)

    max_visits_per_day = Column(Integer, default=5)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
