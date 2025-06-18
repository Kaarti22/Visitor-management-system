from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PreApprovalCreate(BaseModel):
    visitor_id: int
    employee_id: int
    valid_from: datetime
    valid_to: datetime
    max_visits_per_day: Optional[int] = 5

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