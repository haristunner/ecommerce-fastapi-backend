from typing import Optional

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    image_url: str
    category_id: int


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    image_url: str
    rating: float
    is_available: bool
    category_id: int
    is_wishlisted: Optional[bool] = None

    class Config:
        from_attributes = True
