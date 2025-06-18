from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from datetime import datetime

class VisitorCreate(BaseModel):
    full_name: str
    contact: str
    company: Optional[str] = None
    purpose: str
    host_employee_name: str
    host_department: str
    photo_base64: Optional[str] = None

class VisitorOut(BaseModel):
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

    class Config:
        orm_mode = True