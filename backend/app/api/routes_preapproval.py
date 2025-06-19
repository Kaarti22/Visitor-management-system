from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.schemas.preapproval import PreApprovalCreate, PreApprovalOut
from app.services.preapproval_service import PreApprovalService
from app.dependencies.auth_dep import get_current_user

router = APIRouter(prefix="/preapprovals", tags=["PreApprovals"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PreApprovalOut, status_code=status.HTTP_201_CREATED)
def create_preapproval(
    data: PreApprovalCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = PreApprovalService(db)
    if data.employee_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized preapproval attempt")
    pa = service.schedule_visit(**data.dict())
    return pa

@router.get("/{employee_id}", response_model=list[PreApprovalOut])
def list_preapprovals(employee_id: int, db: Session = Depends(get_db)):
    service = PreApprovalService(db)
    return service.list_preapprovals(employee_id)