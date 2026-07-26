from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.connection import Base


class CheckoutItem(Base):
    __tablename__ = "checkout_items"

    id = Column(Integer, primary_key=True, index=True)

    checkout_id = Column(
        Integer,
        ForeignKey("checkouts.id"),
        nullable=False,
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
    )

    quantity = Column(Integer, nullable=False)

    price = Column(Float, nullable=False)

    subtotal = Column(Float, nullable=False)

    checkout = relationship(
        "Checkout",
        back_populates="items",
    )

    product = relationship("Product")
