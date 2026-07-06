from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.connection import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)

    description = Column(Text)

    price = Column(Float, nullable=False)

    stock = Column(Integer, default=0)

    image_url = Column(Text)

    rating = Column(Float, default=0)

    is_available = Column(Boolean, default=True)

    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")

    wishlists = relationship(
        "Wishlist", back_populates="product", cascade="all, delete-orphan"
    )

    cart_items = relationship(
        "Cart", back_populates="product", cascade="all, delete-orphan"
    )

    order_items = relationship("OrderItem", back_populates="product")
