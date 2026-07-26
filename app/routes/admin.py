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


@router.get("/orders")
def get_orders(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        return {"message": "Access Denied"}

    return admin_service.get_admin_orders(db, page=page, limit=limit)


@router.get("/products")
def get_products(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        return {"message": "Access Denied"}

    return admin_service.get_admin_products(db, page=page, limit=limit)


@router.get("/users")
def get_users(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        return {"message": "Access Denied"}

    return admin_service.get_admin_users(db, page=page, limit=limit)


@router.get("/users/{user_id}")
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        return {"message": "Access Denied"}

    user = admin_service.get_admin_user_by_id(db, user_id)
    if user is None:
        return {"message": "User not found"}

    return user
