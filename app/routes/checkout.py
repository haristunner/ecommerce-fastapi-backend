from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.db.connection import get_db
from app.services.auth_service import get_current_user
from app.models.user import User

from app.schemas.checkout import (
    BuyNowCheckoutCreate,
    CheckoutResponse,
    CheckoutUpdate,
)

from app.services.checkout_service import (
    buy_now_checkout,
    checkout_from_cart,
    get_checkout,
    delete_checkout,
    get_checkout_by_id,
    update_checkout,
)


router = APIRouter(
    prefix="/checkout",
    tags=["Checkout"],
)


@router.post(
    "/cart",
    response_model=CheckoutResponse,
)
def create_cart_checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print("Creating cart checkout for user_id:", current_user.id)
    return checkout_from_cart(
        db=db,
        user_id=current_user.id,
    )


@router.post(
    "/buy-now",
    response_model=CheckoutResponse,
)
def create_buy_now_checkout(
    checkout: BuyNowCheckoutCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return buy_now_checkout(
        db=db,
        user_id=current_user.id,
        checkout_data=checkout,
    )


@router.patch("/{id}", response_model=CheckoutResponse)
def patch_checkout(
    id: int,
    checkout: CheckoutUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_checkout(
        id=id, db=db, user_id=current_user.id, checkout_data=checkout
    )


@router.get(
    "/",
    response_model=CheckoutResponse,
)
def get_current_checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_checkout(
        db=db,
        user_id=current_user.id,
    )


@router.get("/{id}", response_model=CheckoutResponse)
def get_checkout_using_id(
    id: int,
    db: Session = Depends(get_db),
):
    return get_checkout_by_id(db, id)


@router.delete("/")
def clear_checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_checkout(
        db=db,
        user_id=current_user.id,
    )
