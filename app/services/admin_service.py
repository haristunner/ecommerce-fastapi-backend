from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload

from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.models.order_item import OrderItem


def get_paginated_items(query, page: int = 1, limit: int = 10):
    page = max(page, 1)
    limit = max(limit, 1)
    total = query.count()
    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
        "data": items,
    }


def get_dashboard(db: Session):

    total_users = db.query(User).count()

    total_products = db.query(Product).count()

    total_categories = db.query(Category).count()

    total_orders = db.query(Order).count()

    pending_orders = db.query(Order).filter(Order.status == "Pending").count()

    completed_orders = db.query(Order).filter(Order.status == "Delivered").count()

    cancelled_orders = db.query(Order).filter(Order.status == "Cancelled").count()

    total_sales = (
        db.query(func.sum(Order.total_amount))
        .filter(Order.status == "Delivered")
        .scalar()
    ) or 0

    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_categories": total_categories,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
        "total_sales": total_sales,
    }


def get_admin_orders(db: Session, page: int = 1, limit: int = 10):
    query = (
        db.query(Order)
        .options(selectinload(Order.order_items).selectinload(OrderItem.product))
        .order_by(Order.created_at.desc())
    )
    return get_paginated_items(query, page=page, limit=limit)


def get_admin_products(db: Session, page: int = 1, limit: int = 10):
    query = db.query(Product).order_by(Product.id.desc())
    return get_paginated_items(query, page=page, limit=limit)


def get_admin_users(db: Session, page: int = 1, limit: int = 10):
    query = db.query(User).order_by(User.created_at.desc())
    return get_paginated_items(query, page=page, limit=limit)


def get_admin_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return None
    return user
