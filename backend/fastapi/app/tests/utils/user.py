import random
import string

from app.schemas.user import UserCreate


def random_lower_string(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email(username_length: int = 8, domain_length: int = 5) -> str:
    username = random_lower_string(username_length)
    domain = random_lower_string(domain_length)
    return f"{username}@{domain}.com" # Not a real email, just for username testing


def get_random_user_create_schema() -> UserCreate:
    username = random_lower_string()
    # In a real app, you might use random_email() for username if format is email
    # For now, using simple random string for username to match current User model
    password = random_lower_string(12)
    return UserCreate(username=username, password=password)

# Function to directly create a user in DB (example, less preferred than API testing for auth)
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.cruds.crud_user import create_user as crud_create_user
# from app.models.user import User as UserModel

# async def create_random_user_in_db(db: AsyncSession) -> UserModel:
#     user_in = get_random_user_create_schema()
#     user = await crud_create_user(db=db, user=user_in)
#     return user
