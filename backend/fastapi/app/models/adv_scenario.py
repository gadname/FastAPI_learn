from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR, Text, ForeignKey
from app.utils.id_generator import generate_ulid
from datetime import datetime
from sqlalchemy import DateTime
from typing import Optional, TYPE_CHECKING # Added Optional

if TYPE_CHECKING:
    from .adv_dialogue import AdvDialogueLine
    from .adv_session import AdvChatSession

class AdvScenario(Base):
    __tablename__ = "adv_scenarios"

    id: Mapped[str] = mapped_column(VARCHAR(26), primary_key=True, index=True, default=generate_ulid)
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    dialogue_lines: Mapped[list["AdvDialogueLine"]] = relationship(back_populates="scenario", foreign_keys="AdvDialogueLine.scenario_id")
    chat_sessions: Mapped[list["AdvChatSession"]] = relationship(back_populates="scenario")
    first_dialogue_line_id: Mapped[str | None] = mapped_column(VARCHAR(26), ForeignKey("adv_dialogue_lines.id"), nullable=True) # Optional: Direct link to the starting dialogue
    first_dialogue_line: Mapped[Optional["AdvDialogueLine"]] = relationship(foreign_keys=[first_dialogue_line_id])
