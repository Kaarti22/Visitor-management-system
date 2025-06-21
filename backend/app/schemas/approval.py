"""
schemas/approval.py — Pydantic schemas for Approval-related operations and responses.
"""

from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime
from app.schemas.visitor import VisitorOut

# Define approval status choices
class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

# Full output schema for an approval record
class ApprovalOut(BaseModel):
    """
    Schema for returning approval details.
    Includes associated visitor object for context.
    """
    id: int
    visitor_id: int
    employee_id: int
    status: ApprovalStatus
    requested_at: datetime
    decision_at: Optional[datetime]
    visitor: Optional[VisitorOut]

    class Config:
        from_attributes = True

# Input schema for updating approval status (approve/reject)
class ApprovalAction(BaseModel):
    """
    Schema for performing an approval action (approve or reject).
    """
    status: ApprovalStatus
