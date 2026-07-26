from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.services.auth_service import get_current_user
from app.models.user import User
from app.schemas.address import (
    AddressCreate,
    AddressUpdate,
    AddressResponse,
)
from app.services.address_service import (
    create_address,
    get_addresses,
    get_address_by_id,
    update_address,
    delete_address,
    set_default_address,
)

router = APIRouter(
    prefix="/user/address",
    tags=["Address"],
)


@router.post("/", response_model=AddressResponse)
def add_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_address(db, current_user.id, address)


@router.get("/", response_model=list[AddressResponse])
def get_all_addresses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_addresses(db, current_user.id)


@router.get("/{address_id}", response_model=AddressResponse)
def get_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_address_by_id(db, address_id, current_user.id)


@router.put("/{address_id}", response_model=AddressResponse)
def edit_address(
    address_id: int,
    address: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_address(
        db,
        address_id,
        current_user.id,
        address,
    )


@router.delete("/{address_id}")
def remove_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_address(
        db,
        address_id,
        current_user.id,
    )


@router.put("/{address_id}/default", response_model=AddressResponse)
def make_default_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return set_default_address(
        db,
        address_id,
        current_user.id,
    )
