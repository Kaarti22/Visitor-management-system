from fastapi import APIRouter, Depends
from app.dependencies.auth_dep import get_current_user

router = APIRouter(prefix="/employee", tags=["Employee"])

@router.get("/dashboard")
def dashboard(current_user = Depends(get_current_user)):
    return {"msg": f"Hello {current_user['sub']} (employee id: {current_user['id']})"}