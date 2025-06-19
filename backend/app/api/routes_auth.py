from fastapi import APIRouter, HTTPException, status, Depends, Form
from app.core.config import SessionLocal
from sqlalchemy.orm import Session
from app.utils.auth import verify_password, create_access_token
from app.models import Employee

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    employee = db.query(Employee).filter_by(email=email).first()
    if not employee or not verify_password(password, employee.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": employee.email, "id": employee.id})
    return {"access_token": token, "token_type": "bearer"}