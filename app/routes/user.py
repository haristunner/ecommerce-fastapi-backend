from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.schemas.user import UserCreate, UserResponse, TokenResponse, UserLogin
from app.services.user_service import create_user, authenticate_user
from app.utils.jwt import create_access_token
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    created_user = create_user(db, user)

    if created_user is None:
        raise HTTPException(status_code=400, detail="Email already exists")

    return created_user


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = authenticate_user(db, user.email, user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(
        {"sub": str(db_user.id), "email": db_user.email, "role": db_user.role}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "is_admin": db_user.role == "admin",
    }


@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user
