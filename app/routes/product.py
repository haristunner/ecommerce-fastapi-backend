from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.services.product_service import add_product, get_products, get_product_by_id
from app.schemas.product import ProductCreate, ProductResponse
from app.models.user import User
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
def get_all_products(
    search: str = None,
    category_id: int = None,
    min_price: float = None,
    max_price: float = None,
    sort: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return get_products(
        db=db,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        sort=sort,
        page=page,
        limit=limit,
    )


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_product_by_id(db, product_id, current_user.id)


@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):

    return add_product(db=db, product=product)
