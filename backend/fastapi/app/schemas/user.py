from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema for token data embedded in JWT
class TokenData(BaseModel):
    username: Optional[str] = None

# Schema for the token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Base schema for User properties
class UserBase(BaseModel):
    username: str
    email: EmailStr

# Schema for user creation (request)
# Expects a plain password
class UserCreate(UserBase):
    password: str

# Schema for reading/returning user data (response)
# Does not include password
class User(UserBase):
    id: int

    class Config:
        orm_mode = True # For Pydantic V1, use from_attributes = True for V2
        # For Pydantic V2, it's from_attributes = True
        # Ensure your Pydantic version matches this configuration.
        # If using Pydantic V1 and it doesn't work, try 'from_orm = True'
        # If Pydantic V2, and 'from_attributes = True' causes issues,
        # consult Pydantic docs for the correct ORM mode setting.
        # Given the project structure, 'orm_mode = True' is common for Pydantic V1.x.
        # Let's assume Pydantic V1 for now. If there's an error, we might need to adjust.
