from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.connection import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    full_name = Column(String, nullable=False)
    mobile_number = Column(String(15), nullable=False)

    address_line_1 = Column(String, nullable=False)
    address_line_2 = Column(String)

    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    pincode = Column(String(10), nullable=False)

    landmark = Column(String)

    address_type = Column(String, default="Home")

    is_default = Column(Boolean, default=False)

    user = relationship("User", back_populates="addresses")
