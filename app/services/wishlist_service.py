from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.wishlist import Wishlist
from app.models.product import Product


def add_to_wishlist(db: Session, user_id: int, product_id: int):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = (
        db.query(Wishlist)
        .filter(Wishlist.user_id == user_id, Wishlist.product_id == product_id)
        .first()
    )

    if existing:
        raise HTTPException(status_code=400, detail="Product already in wishlist")

    wishlist = Wishlist(user_id=user_id, product_id=product_id)

    db.add(wishlist)
    db.commit()
    db.refresh(wishlist)

    return wishlist


def get_wishlist(db: Session, user_id: int):

    return (
        db.query(Wishlist)
        .options(joinedload(Wishlist.product))
        .filter(Wishlist.user_id == user_id)
        .all()
    )


def remove_from_wishlist(db: Session, user_id: int, product_id: int):

    wishlist = (
        db.query(Wishlist)
        .filter(Wishlist.user_id == user_id, Wishlist.product_id == product_id)
        .first()
    )

    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist item not found")

    db.delete(wishlist)
    db.commit()

    return {"message": "Product removed from wishlist"}
