from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import DateTime, VARCHAR
from sqlalchemy.sql import func
from app.utils.id_generator import generate_ulid


class ChatBot(Base):
    __tablename__ = "chat_bots"

    id: Mapped[str] = mapped_column(
        VARCHAR(26),
        index=True,
        nullable=False,
        unique=True,
        default=generate_ulid,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    color: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
