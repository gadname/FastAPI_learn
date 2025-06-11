from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR, ForeignKey
from app.utils.id_generator import generate_ulid
from datetime import datetime
from sqlalchemy import DateTime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .adv_dialogue import AdvDialogueLine
    from .adv_scenario import AdvScenario

class AdvChatSession(Base):
    __tablename__ = "adv_chat_sessions"

    id: Mapped[str] = mapped_column(VARCHAR(26), primary_key=True, index=True, default=generate_ulid)
    scenario_id: Mapped[str] = mapped_column(ForeignKey("adv_scenarios.id"), nullable=False)
    current_dialogue_line_id: Mapped[str] = mapped_column(ForeignKey("adv_dialogue_lines.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    scenario: Mapped["AdvScenario"] = relationship(back_populates="chat_sessions")
    current_dialogue_line: Mapped["AdvDialogueLine"] = relationship(foreign_keys=[current_dialogue_line_id])
