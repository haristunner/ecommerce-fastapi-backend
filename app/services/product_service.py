from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate
from app.models.wishlist import Wishlist


def get_products(
    db: Session,
    search: str = None,
    category_id: int = None,
    min_price: float = None,
    max_price: float = None,
    sort: str = None,
    page: int = 1,
    limit: int = 10,
):

    query = db.query(Product)

    # Search by product name
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    # Filter by category
    if category_id:
        query = query.filter(Product.category_id == category_id)

    # Filter by minimum price
    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    # Filter by maximum price
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    # Sort
    if sort == "price_asc":
        query = query.order_by(asc(Product.price))

    elif sort == "price_desc":
        query = query.order_by(desc(Product.price))

    elif sort == "name_asc":
        query = query.order_by(asc(Product.name))

    elif sort == "name_desc":
        query = query.order_by(desc(Product.name))

    else:
        query = query.order_by(desc(Product.id))

    # Total count before pagination
    total = query.count()

    # Pagination
    offset = (page - 1) * limit

    products = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
        "data": products,
    }


def get_product_by_id(db: Session, product_id: int, user_id: int):

    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    is_wishlisted = (
        db.query(Wishlist)
        .filter(
            Wishlist.user_id == user_id,
            Wishlist.product_id == product_id,
        )
        .first()
        is not None
    )

    print(f"Is product {product_id} wishlisted by user {user_id}? {is_wishlisted}")

    return {**product.__dict__, "is_wishlisted": is_wishlisted}


def add_product(db: Session, product: ProductCreate):

    category = db.query(Category).filter(Category.id == product.category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        image_url=product.image_url,
        category_id=product.category_id,
        rating=0,
        is_available=True,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product
