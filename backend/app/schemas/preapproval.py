"""
schemas/preapproval.py — Pydantic schemas for creating and returning pre-approval data.
"""

from pydantic import BaseModel, validator
from datetime import datetime, timezone
from typing import Optional


class PreApprovalCreate(BaseModel):
    """
    Schema used when an employee schedules a pre-approval.
    """
    visitor_id: int
    employee_id: int
    valid_from: datetime
    valid_to: datetime
    max_visits_per_day: Optional[int] = 5

    @validator("valid_from", "valid_to", pre=True)
    def ensure_utc(cls, value):
        """
        Converts naive or ISO-formatted datetimes to timezone-aware UTC.
        Ensures consistency during DB writes and comparisons.
        """
        if isinstance(value, str):
            dt = datetime.fromisoformat(value)
            if not dt.tzinfo:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        return value


class PreApprovalOut(BaseModel):
    """
    Schema for returning pre-approval information to the frontend or admin.
    """
    id: int
    visitor_id: int
    employee_id: int
    valid_from: datetime
    valid_to: datetime
    max_visits_per_day: int
    created_at: datetime

    class Config:
        from_attributes = True  # Correct attribute to enable ORM serialization
