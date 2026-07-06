from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services import wishlist_service
from app.schemas.wishlist import WishlistResponse

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.post("/{product_id}")
def add_to_wishlist(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return wishlist_service.add_to_wishlist(
        db=db, user_id=current_user.id, product_id=product_id
    )


@router.get("/", response_model=list[WishlistResponse])
def get_wishlist(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):

    return wishlist_service.get_wishlist(db=db, user_id=current_user.id)


@router.delete("/{product_id}")
def remove_from_wishlist(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return wishlist_service.remove_from_wishlist(
        db=db, user_id=current_user.id, product_id=product_id
    )
