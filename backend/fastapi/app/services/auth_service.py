from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds import crud_user
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import (
    create_access_token,
    verify_password,
)


async def register_new_user(db: AsyncSession, user_create: UserCreate) -> User:
    db_user = await crud_user.get_user_by_username(db, username=user_create.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    new_user = await crud_user.create_user(db, user=user_create)
    return new_user


async def authenticate_user(db: AsyncSession, username: str, password: str) -> User | None:
    user = await crud_user.get_user_by_username(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_jwt_token(user: User) -> dict:
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
