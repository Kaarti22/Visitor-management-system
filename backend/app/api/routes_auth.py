"""
api/routes_auth.py — Handles user authentication (JWT login) for employees.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.utils.auth import verify_password, create_access_token
from app.models import Employee
from app.schemas.auth_schemas import LoginInput, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    """
    Dependency that provides a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginInput,
    db: Session = Depends(get_db)
):
    """
    Logs in an employee and returns a JWT access token.

    - Verifies credentials against stored hashed passwords.
    - On success, returns a Bearer token with employee ID embedded in payload.
    """
    email = data.email
    password = data.password

    employee = db.query(Employee).filter_by(email=email).first()

    if not employee or not verify_password(password, employee.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token({"sub": employee.email, "id": employee.id})

    return TokenResponse(access_token=token, token_type="bearer")
