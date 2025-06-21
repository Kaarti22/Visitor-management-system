"""
api/routes_employee.py — Routes for employee-related actions, including dashboard access.
"""

from fastapi import APIRouter, Depends
from app.dependencies.auth_dep import get_current_user

router = APIRouter(prefix="/employee", tags=["Employee"])

@router.get("/dashboard")
def dashboard(current_user=Depends(get_current_user)):
    """
    Dashboard for logged-in employees.

    - Protected by JWT authentication
    - Returns a personalized greeting with employee ID
    """
    return {
        "msg": f"Hello {current_user['sub']} (employee id: {current_user['id']})"
    }
