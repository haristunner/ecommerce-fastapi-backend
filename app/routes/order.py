from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.models.user import User
from app.schemas.order import (
    PlaceOrderRequest,
    OrderResponse,
)
from app.services.auth_service import get_current_user
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=list[OrderResponse])
def place_order(
    order: PlaceOrderRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return order_service.place_order(
        db=db,
        user_id=current_user.id,
        shipping_address=order.shipping_address,
    )


@router.get("/", response_model=list[OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return order_service.get_orders(
        db=db,
        user_id=current_user.id,
    )


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return order_service.get_order_by_id(
        db=db,
        user_id=current_user.id,
        order_id=order_id,
    )


@router.put("/{order_id}/cancel")
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return order_service.cancel_order(
        db=db,
        user_id=current_user.id,
        order_id=order_id,
    )
