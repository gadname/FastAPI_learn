from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

# Direct imports for schemas
from app.schemas.user import User as UserSchema, UserCreate as UserCreateSchema, Token as TokenSchema
from app.cruds.crud_user import user as crud_user
from app.db.database import get_db
from app.utils.security import create_access_token, verify_password
# from app.settings import settings # Not directly used in this version of auth.py, but often needed

router = APIRouter()

@router.post("/register", response_model=UserSchema)
async def register_user(
    user_in: UserCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    existing_user_by_username = await crud_user.get_user_by_username(db, username=user_in.username)
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Pydantic's EmailStr should handle validation, but ensure it's string for DB
    existing_user_by_email = await crud_user.get_user_by_email(db, email=str(user_in.email))
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = await crud_user.create_user(db=db, obj_in=user_in)
    return user

@router.post("/login", response_model=TokenSchema)
async def login_for_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await crud_user.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}
