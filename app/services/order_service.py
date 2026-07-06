from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.cart import Cart
from app.models.order import Order
from app.models.order_item import OrderItem


def place_order(db: Session, user_id: int, shipping_address: str):

    # Get cart items
    cart_items = (
        db.query(Cart)
        .options(joinedload(Cart.product))
        .filter(Cart.user_id == user_id)
        .all()
    )

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = 0

    # Validate stock
    for item in cart_items:
        if item.quantity > item.product.stock:
            raise HTTPException(
                status_code=400,
                detail=f"{item.product.name} has only {item.product.stock} items left",
            )

        total_amount += item.quantity * item.product.price

    # Create order
    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="Pending",
        payment_status="Pending",
        shipping_address=shipping_address,
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    # Create order items
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price,
            subtotal=item.quantity * item.product.price,
        )

        db.add(order_item)

        # Reduce stock
        item.product.stock -= item.quantity

    # Clear cart
    db.query(Cart).filter(Cart.user_id == user_id).delete()

    db.commit()

    db.refresh(order)

    return order


def get_orders(db: Session, user_id: int):

    orders = (
        db.query(Order)
        .options(joinedload(Order.order_items).joinedload(OrderItem.product))
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .all()
    )

    return orders


def get_order_by_id(db: Session, user_id: int, order_id: int):

    order = (
        db.query(Order)
        .options(joinedload(Order.order_items).joinedload(OrderItem.product))
        .filter(Order.id == order_id, Order.user_id == user_id)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


def cancel_order(db: Session, user_id: int, order_id: int):

    order = (
        db.query(Order)
        .options(joinedload(Order.order_items).joinedload(OrderItem.product))
        .filter(Order.id == order_id, Order.user_id == user_id)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status not in ["Pending", "Confirmed"]:
        raise HTTPException(status_code=400, detail="Order cannot be cancelled")

    # Restore product stock
    for item in order.order_items:
        item.product.stock += item.quantity

    order.status = "Cancelled"

    db.commit()
    db.refresh(order)

    return {"message": "Order cancelled successfully"}
