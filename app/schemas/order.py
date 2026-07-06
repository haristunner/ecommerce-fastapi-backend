from datetime import datetime
from pydantic import BaseModel


class PlaceOrderRequest(BaseModel):
    shipping_address: str


class OrderProductResponse(BaseModel):
    id: int
    name: str
    price: float
    image_url: str | None = None

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
    total_amount: float
    status: str
    payment_status: str
    shipping_address: str
    created_at: datetime
    order_items: list[OrderItemResponse]

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    id: int
    total_amount: float
    status: str
    payment_status: str
    created_at: datetime

    class Config:
        from_attributes = True
