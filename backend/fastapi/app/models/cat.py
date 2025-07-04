from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.database import Base
from app.utils.id_generator import generate_ulid
from sqlalchemy import VARCHAR


class Cat(Base):
    __tablename__ = "cats"

    id: Mapped[str] = mapped_column(
        VARCHAR(26),
        index=True,
        nullable=False,
        unique=True,
        default=generate_ulid,
        primary_key=True,
    )
    name = Column(String, nullable=False)
    breed = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
