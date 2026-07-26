from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class PlaceOrderRequest(BaseModel):
    address_id: int
    payment_method: str
    payment_details: Optional[Dict[str, Any]] = None


class OrderProductResponse(BaseModel):
    id: int
    name: str
    price: float
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class OrderItemResponse(BaseModel):
    id: int
    quantity: int
    price: float
    subtotal: float
    product: OrderProductResponse

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    address_id: Optional[int]
    payment_method: Optional[str]
    payment_details: Optional[Dict[str, Any]]
    total_amount: float
    created_at: datetime
    updated_at: datetime
    order_items: List[OrderItemResponse]

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
