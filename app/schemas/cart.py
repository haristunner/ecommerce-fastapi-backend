from pydantic import BaseModel


class AddToCart(BaseModel):
    product_id: int
    quantity: int = 1


class UpdateCart(BaseModel):
    quantity: int


class CartProduct(BaseModel):
    id: int
    name: str
    price: float
    image_url: str | None = None
    stock: int

    class Config:
        from_attributes = True


class CartItemResponse(BaseModel):
    id: int
    quantity: int
    subtotal: float
    product: CartProduct


class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total_items: int
    grand_total: float
