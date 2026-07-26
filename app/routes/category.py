from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category_service import (
    create_category,
    delete_category,
    get_categories,
    update_category,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse)
def add_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category)


@router.get("/", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return get_categories(db)


@router.put("/{category_id}", response_model=CategoryResponse)
def edit_category(
    category_id: int, category: CategoryCreate, db: Session = Depends(get_db)
):
    return update_category(db, category_id, category)


@router.delete("/{category_id}")
def remove_category(category_id: int, db: Session = Depends(get_db)):
    return delete_category(db, category_id)
