from fastapi import APIRouter

from .user import router as auth_router
from .category import router as category_router
from .product import router as product_router
from .wishlist import router as wishlist_router
from .cart import router as cart_router
from .order import router as order_router
from .admin import router as admin_router
from .address import router as address_router
from .checkout import router as checkout_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(category_router)
api_router.include_router(product_router)
api_router.include_router(wishlist_router)
api_router.include_router(cart_router)
api_router.include_router(order_router)
api_router.include_router(admin_router)
api_router.include_router(address_router)
api_router.include_router(checkout_router)
