from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select # For SQLAlchemy 2.0+

from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash

class CRUDUser:
    async def get_user_by_username(self, db: AsyncSession, *, username: str) -> User | None:
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

    async def get_user_by_email(self, db: AsyncSession, *, email: str) -> User | None:
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def create_user(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        hashed_password = get_password_hash(obj_in.password)
        # Ensure obj_in.username and obj_in.email are strings
        db_obj = User(
            username=str(obj_in.username),
            email=str(obj_in.email), # Pydantic's EmailStr should be fine, but explicit str() is safe
            hashed_password=hashed_password,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

user = CRUDUser()
