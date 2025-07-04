from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import TokenData
from app.utils.security import decode_access_token # Using the one from security.py
from app.cruds.crud_user import user as crud_user # Import the CRUD user instance
# from app.settings import settings # Not directly used here but often for SECRET_KEY, ALGORITHM if not in decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login") # Adjusted tokenUrl to match auth router

async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = decode_access_token(token) # This was created in security.py

    if token_data is None or token_data.username is None: # Check if token_data or username is None
        raise credentials_exception

    user = await crud_user.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    # If you add an `is_active` field to the User model, you can check it here.
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Example of how to use it in an endpoint (not part of this subtask):
# from app.api.deps import get_current_active_user
# @router.get("/users/me", response_model=UserSchema)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user
