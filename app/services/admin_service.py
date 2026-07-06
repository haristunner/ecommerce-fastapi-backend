from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order


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
