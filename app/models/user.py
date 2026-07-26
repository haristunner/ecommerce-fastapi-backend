from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(150), unique=True, nullable=False, index=True)

    password = Column(String(255), nullable=False)

    mobile_number = Column(String(15), nullable=True)

    role = Column(String(20), default="user")

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    wishlists = relationship(
        "Wishlist", back_populates="user", cascade="all, delete-orphan"
    )

    cart_items = relationship(
        "Cart", back_populates="user", cascade="all, delete-orphan"
    )

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
