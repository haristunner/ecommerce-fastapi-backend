from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.services.auth_service import get_current_user
from app.services import admin_service
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        return {"message": "Access Denied"}

    return admin_service.get_dashboard(db)
