from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.models.user import User
from app.schemas.cart import AddToCart, UpdateCart, CartResponse
from app.services.auth_service import get_current_user
from app.services import cart_service

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/")
def add_to_cart(
    cart: AddToCart,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return cart_service.add_to_cart(db=db, user_id=current_user.id, cart=cart)


@router.get("/", response_model=CartResponse)
def get_cart(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):

    return cart_service.get_cart(db=db, user_id=current_user.id)


@router.put("/{product_id}")
def update_cart(
    product_id: int,
    cart: UpdateCart,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return cart_service.update_cart(
        db=db, user_id=current_user.id, product_id=product_id, quantity=cart.quantity
    )


@router.delete("/{product_id}")
def remove_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return cart_service.remove_from_cart(
        db=db, user_id=current_user.id, product_id=product_id
    )


@router.delete("/")
def clear_cart(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):

    return cart_service.clear_cart(db=db, user_id=current_user.id)
