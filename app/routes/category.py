from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category_service import (
    create_category,
    get_categories
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("/", response_model=CategoryResponse)
def add_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    return create_category(db, category)


@router.get("/", response_model=list[CategoryResponse])
def list_categories(
    db: Session = Depends(get_db)
):
    return get_categories(db)