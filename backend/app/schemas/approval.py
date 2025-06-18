from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class ApprovalOut(BaseModel):
    id: int
    visitor_id: int
    employee_id: int
    status: ApprovalStatus
    requested_at: datetime
    decision_at: Optional[datetime]

    class Config:
        orm_mode = True

class ApprovalAction(BaseModel):
    status: ApprovalStatus