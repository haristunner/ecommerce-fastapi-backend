from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate


def create_category(db: Session, category: CategoryCreate):

    new_category = Category(name=category.name, description=category.description)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


def get_categories(db: Session):
    return db.query(Category).all()


def update_category(db: Session, category_id: int, category: CategoryCreate):
    category_record = db.query(Category).filter(Category.id == category_id).first()

    if not category_record:
        raise HTTPException(status_code=404, detail="Category not found")

    category_record.name = category.name
    category_record.description = category.description

    db.commit()
    db.refresh(category_record)

    return category_record


def delete_category(db: Session, category_id: int):
    category_record = db.query(Category).filter(Category.id == category_id).first()

    if not category_record:
        raise HTTPException(status_code=404, detail="Category not found")

    if category_record.products:
        raise HTTPException(
            status_code=400, detail="Cannot delete category with existing products"
        )

    db.delete(category_record)
    db.commit()

    return {"message": "Category deleted"}
