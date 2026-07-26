from sqlalchemy import JSON, Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.connection import Base


class Checkout(Base):
    __tablename__ = "checkouts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)

    payment_method = Column(String, nullable=True)
    total_amount = Column(Float, nullable=False)

    payment_details = Column(JSON, nullable=True)

    checkout_type = Column(
        Enum("cart", "buy_now", name="checkout_type"),
        nullable=False,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user = relationship("User")
    address = relationship("Address")

    items = relationship(
        "CheckoutItem",
        back_populates="checkout",
        cascade="all, delete-orphan",
    )
