from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.schemas.user import TokenData # Import TokenData from user schemas
from app.settings import settings # Import settings to access JWT secret etc.

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Or fetch from settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Ensure settings.SECRET_KEY and settings.ALGORITHM are available
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Function to decode token and get TokenData (could be expanded for full user retrieval later in deps.py)
def decode_access_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: Optional[str] = payload.get("sub") # Assuming 'sub' is the username
        if username is None:
            return None # Or raise credentials_exception
        return TokenData(username=username)
    except JWTError:
        return None # Or raise credentials_exception
