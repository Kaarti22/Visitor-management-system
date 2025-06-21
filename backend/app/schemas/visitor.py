"""
schemas/visitor.py — Pydantic schemas for Visitor registration, retrieval, and response models.
"""

from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


class VisitorCreate(BaseModel):
    """
    Schema for creating a new visitor registration.
    Sent from frontend to backend during registration.
    """
    full_name: str
    contact: str
    company: Optional[str] = None
    purpose: str
    host_employee_name: str
    host_department: str
    photo_base64: str  # base64-encoded photo string


class VisitorOut(BaseModel):
    """
    Schema for returning visitor details.
    Includes optional approval info and badge URLs.
    """
    id: int
    full_name: str
    contact: str
    company: Optional[str]
    purpose: str
    host_employee_name: str
    host_department: str
    photo_url: Optional[HttpUrl]
    badge_url: Optional[HttpUrl]
    check_in: datetime
    check_out: Optional[datetime]
    created_at: datetime
    approval: Optional["ApprovalOut"] = None  # forward ref

    class Config:
        from_attributes = True


# Import after class definition to resolve circular reference
from app.schemas.approval import ApprovalOut
VisitorOut.update_forward_refs()
