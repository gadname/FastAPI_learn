from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas import user as user_schema
from app.schemas import token as token_schema
from app.services import auth_service
from app.utils import security

router = APIRouter()


@router.post("/register", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: user_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    db_user = await auth_service.register_new_user(db=db, user_create=user_in)
    if not db_user: # Should be handled by service, but as a safeguard
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create user",
        )
    return db_user


@router.post("/login", response_model=token_schema.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
):
    user = await auth_service.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = auth_service.create_jwt_token(user=user)
    return token_schema.Token(**token_data)


@router.get("/users/me", response_model=user_schema.User)
async def read_users_me(
    current_user: Annotated[user_schema.User, Depends(security.get_current_user)],
):
    return current_user
