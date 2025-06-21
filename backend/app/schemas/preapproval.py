from pydantic import BaseModel, validator
from datetime import datetime, timezone
from typing import Optional

class PreApprovalCreate(BaseModel):
    visitor_id: int
    employee_id: int
    valid_from: datetime
    valid_to: datetime
    max_visits_per_day: Optional[int] = 5

    @validator("valid_from", "valid_to", pre=True)
    def ensure_utc(cls, v):
        if isinstance(v, str):
            dt = datetime.fromisoformat(v)
            if not dt.tzinfo:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        return v

class PreApprovalOut(BaseModel):
    id: int
    visitor_id: int
    employee_id: int
    valid_from: datetime
    valid_to: datetime
    max_visits_per_day: int
    created_at: datetime

    class Config:
        orm_model = True