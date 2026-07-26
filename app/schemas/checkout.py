from datetime import datetime
from typing import Any, Dict, Optional, List

from pydantic import BaseModel

from app.schemas.product import ProductResponse
from app.schemas.address import AddressResponse


# ---------- Request Schemas ----------


class BuyNowCheckoutCreate(BaseModel):
    product_id: int
    quantity: int


class CheckoutUpdate(BaseModel):
    address_id: int
    payment_method: str
    payment_details: Optional[Dict[str, Any]] = None


# ---------- Response Schemas ----------


class CheckoutItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    subtotal: float

    product: ProductResponse

    class Config:
        from_attributes = True


class CheckoutResponse(BaseModel):
    id: int

    user_id: int
    address_id: Optional[int]

    payment_method: Optional[str]

    total_amount: float

    created_at: datetime
    updated_at: datetime

    address: Optional[AddressResponse] = None

    items: List[CheckoutItemResponse]

    class Config:
        from_attributes = True
