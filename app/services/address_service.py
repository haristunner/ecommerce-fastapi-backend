from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate


def create_address(db: Session, user_id: int, address: AddressCreate):
    # If first address, make it default
    is_default = address.is_default

    existing = db.query(Address).filter(Address.user_id == user_id).count()
    if existing == 0:
        is_default = True

    # If setting new default, remove existing default
    if is_default:
        db.query(Address).filter(Address.user_id == user_id, Address.is_default).update(
            {"is_default": False}
        )

    new_address = Address(
        user_id=user_id,
        full_name=address.full_name,
        mobile_number=address.mobile_number,
        address_line_1=address.address_line_1,
        address_line_2=address.address_line_2,
        city=address.city,
        state=address.state,
        pincode=address.pincode,
        landmark=address.landmark,
        address_type=address.address_type,
        is_default=is_default,
    )

    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    return new_address


def get_addresses(db: Session, user_id: int):
    return (
        db.query(Address)
        .filter(Address.user_id == user_id)
        .order_by(Address.is_default.desc(), Address.id.desc())
        .all()
    )


def get_address_by_id(db: Session, address_id: int, user_id: int):
    address = (
        db.query(Address)
        .filter(Address.id == address_id, Address.user_id == user_id)
        .first()
    )

    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )

    return address


def update_address(db: Session, address_id: int, user_id: int, payload: AddressUpdate):
    address = get_address_by_id(db, address_id, user_id)

    if payload.is_default:
        db.query(Address).filter(Address.user_id == user_id).update(
            {"is_default": False}
        )

        address.is_default = True

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(address, key, value)

    db.commit()
    db.refresh(address)

    return address


def delete_address(db: Session, address_id: int, user_id: int):
    address = get_address_by_id(db, address_id, user_id)

    was_default = address.is_default

    db.delete(address)
    db.commit()

    if was_default:
        first_address = db.query(Address).filter(Address.user_id == user_id).first()

        if first_address:
            first_address.is_default = True
            db.commit()

    return {"message": "Address deleted successfully"}


def set_default_address(db: Session, address_id: int, user_id: int):
    address = get_address_by_id(db, address_id, user_id)

    db.query(Address).filter(Address.user_id == user_id).update({"is_default": False})

    address.is_default = True

    db.commit()
    db.refresh(address)

    return address
