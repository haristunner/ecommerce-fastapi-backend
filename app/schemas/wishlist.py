from pydantic import BaseModel


class WishlistProduct(BaseModel):
    id: int
    name: str
    price: float
    image_url: str | None = None

    class Config:
        from_attributes = True


class WishlistResponse(BaseModel):
    id: int
    product: WishlistProduct

    class Config:
        from_attributes = True
