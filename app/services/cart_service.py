from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.cart import Cart
from app.models.product import Product
from app.schemas.cart import AddToCart


def add_to_cart(db: Session, user_id: int, cart: AddToCart):

    product = db.query(Product).filter(Product.id == cart.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_item = (
        db.query(Cart)
        .filter(Cart.user_id == user_id, Cart.product_id == cart.product_id)
        .first()
    )

    if cart_item:
        cart_item.quantity += cart.quantity
    else:
        cart_item = Cart(
            user_id=user_id, product_id=cart.product_id, quantity=cart.quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return cart_item


def get_cart(db: Session, user_id: int):

    cart_items = (
        db.query(Cart)
        .options(joinedload(Cart.product))
        .filter(Cart.user_id == user_id)
        .all()
    )

    print("Cart_items::", cart_items)

    items = []
    grand_total = 0
    total_items = 0

    for item in cart_items:
        subtotal = item.quantity * item.product.price

        grand_total += subtotal
        total_items += item.quantity

        items.append(
            {
                "id": item.id,
                "quantity": item.quantity,
                "subtotal": subtotal,
                "product": {
                    "id": item.product.id,
                    "name": item.product.name,
                    "price": item.product.price,
                    "image_url": item.product.image_url,
                    "stock": item.product.stock,
                },
            }
        )

    return {"items": items, "total_items": total_items, "grand_total": grand_total}


def update_cart(db: Session, user_id: int, product_id: int, quantity: int):

    cart_item = (
        db.query(Cart)
        .filter(Cart.user_id == user_id, Cart.product_id == product_id)
        .first()
    )

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.quantity = quantity

    db.commit()
    db.refresh(cart_item)

    return cart_item


def remove_from_cart(db: Session, user_id: int, product_id: int):

    cart_item = (
        db.query(Cart)
        .filter(Cart.user_id == user_id, Cart.product_id == product_id)
        .first()
    )

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()

    return {"message": "Product removed from cart"}


def clear_cart(db: Session, user_id: int):

    db.query(Cart).filter(Cart.user_id == user_id).delete()

    db.commit()

    return {"message": "Cart cleared successfully"}
