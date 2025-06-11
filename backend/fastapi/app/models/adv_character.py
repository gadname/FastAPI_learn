from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR, ForeignKey, Text
from app.utils.id_generator import generate_ulid
from datetime import datetime
from sqlalchemy import DateTime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .adv_dialogue import AdvDialogueLine

class AdvCharacter(Base):
    __tablename__ = "adv_characters"

    id: Mapped[str] = mapped_column(VARCHAR(26), primary_key=True, index=True, default=generate_ulid)
    name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False, unique=True) # e.g., "User", "BotName", "Narrator"
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    dialogue_lines: Mapped[list["AdvDialogueLine"]] = relationship(back_populates="character")
