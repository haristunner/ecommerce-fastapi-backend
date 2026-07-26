from fastapi import HTTPException
from sqlalchemy.orm import Session

# from app.models.cart import Cart
from app.models.checkout import Checkout
from app.models.checkout_item import CheckoutItem
from app.models.product import Product

from app.schemas.checkout import (
    BuyNowCheckoutCreate,
    CheckoutUpdate,
)
from app.services.cart_service import get_cart
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.cart import Cart


def delete_checkout(db: Session, user_id: int):
    checkout = db.query(Checkout).filter(Checkout.user_id == user_id).first()
    print("Checkout::", checkout)

    if checkout:
        (
            db.query(CheckoutItem)
            .filter(CheckoutItem.checkout_id == checkout.id)
            .delete(synchronize_session=False)
        )

        db.delete(checkout)
        db.commit()

    return {"message": "Checkout cleared successfully"}


def get_checkout(db: Session, user_id: int):
    checkout = db.query(Checkout).filter(Checkout.user_id == user_id).first()

    if checkout is None:
        raise HTTPException(
            status_code=404,
            detail="Checkout not found",
        )

    return checkout


def checkout_from_cart(
    db: Session,
    user_id: int,
):
    deleted_checkout = delete_checkout(db, user_id)
    print("Deleted:", deleted_checkout)

    cart = get_cart(db, user_id)

    print("Cart::", cart)

    if not cart.get("items"):
        raise HTTPException(
            status_code=400,
            detail="Cart is empty",
        )

    total_amount = cart["grand_total"]

    checkout = Checkout(
        user_id=user_id, total_amount=total_amount, checkout_type="cart"
    )

    db.add(checkout)
    db.flush()

    for item in cart["items"]:
        db.add(
            CheckoutItem(
                checkout_id=checkout.id,
                product_id=item["product"]["id"],
                quantity=item["quantity"],
                price=item["product"]["price"],
                subtotal=item["subtotal"],
            )
        )

    db.commit()
    db.refresh(checkout)

    return checkout


def buy_now_checkout(
    db: Session,
    user_id: int,
    checkout_data: BuyNowCheckoutCreate,
):
    delete_checkout(db, user_id)

    product = db.query(Product).filter(Product.id == checkout_data.product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    subtotal = product.price * checkout_data.quantity

    checkout = Checkout(
        user_id=user_id,
        total_amount=subtotal,
        checkout_type="buy_now",
    )

    db.add(checkout)
    db.flush()

    db.add(
        CheckoutItem(
            checkout_id=checkout.id,
            product_id=product.id,
            quantity=checkout_data.quantity,
            price=product.price,
            subtotal=subtotal,
        )
    )

    db.commit()
    db.refresh(checkout)

    return checkout


def update_checkout(
    id: int,
    db: Session,
    user_id: int,
    checkout_data: CheckoutUpdate,
):
    checkout = db.query(Checkout).filter(Checkout.id == id).first()

    if checkout is None:
        raise HTTPException(
            status_code=404,
            detail="Checkout not found",
        )

    checkout.address_id = checkout_data.address_id
    checkout.payment_method = checkout_data.payment_method
    checkout.payment_details = checkout_data.payment_details

    db.commit()
    db.refresh(checkout)

    # Create Order
    if checkout.address_id is not None and checkout.payment_method:
        order = Order(
            user_id=user_id,
            address_id=checkout.address_id,
            payment_method=checkout.payment_method,
            payment_details=checkout.payment_details,
            total_amount=checkout.total_amount,
        )

        db.add(order)
        db.flush()

        for item in checkout.items:
            db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price,
                    subtotal=item.subtotal,
                )
            )

        db.commit()
        db.refresh(order)

        if checkout.checkout_type == "cart":
            for item in checkout.items:
                db.query(Cart).filter(
                    Cart.user_id == user_id,
                    Cart.product_id == item.product_id,
                ).delete(synchronize_session=False)

            db.commit()

    return checkout


def get_checkout_by_id(db: Session, checkout_id: int):
    checkout = db.query(Checkout).filter(Checkout.id == checkout_id).first()

    if checkout is None:
        raise HTTPException(
            status_code=404,
            detail="Checkout not found",
        )

    return checkout
