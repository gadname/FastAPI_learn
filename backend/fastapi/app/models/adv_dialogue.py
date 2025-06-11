from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR, Text, Integer, ForeignKey
from app.utils.id_generator import generate_ulid
from datetime import datetime
from sqlalchemy import DateTime
from typing import Optional, TYPE_CHECKING # Added Optional

if TYPE_CHECKING:
    from .adv_scenario import AdvScenario
    from .adv_character import AdvCharacter

class AdvDialogueLine(Base):
    __tablename__ = "adv_dialogue_lines"

    id: Mapped[str] = mapped_column(VARCHAR(26), primary_key=True, index=True, default=generate_ulid)
    scenario_id: Mapped[str] = mapped_column(ForeignKey("adv_scenarios.id"), nullable=False)
    character_id: Mapped[str | None] = mapped_column(ForeignKey("adv_characters.id"), nullable=True) # Nullable if it's a narrator line without a specific character
    text: Mapped[str] = mapped_column(Text, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False) # To maintain sequence within a scenario if not using choices for everything
    emotion: Mapped[str | None] = mapped_column(VARCHAR(50), nullable=True) # e.g., "happy", "sad", "angry"
    pose: Mapped[str | None] = mapped_column(VARCHAR(50), nullable=True) # e.g., "standing", "sitting"
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    scenario: Mapped["AdvScenario"] = relationship(back_populates="dialogue_lines", foreign_keys=[scenario_id])
    character: Mapped[Optional["AdvCharacter"]] = relationship(back_populates="dialogue_lines", foreign_keys=[character_id])

    choices_offered: Mapped[list["AdvChoice"]] = relationship(back_populates="source_dialogue_line", foreign_keys="AdvChoice.source_dialogue_line_id")


class AdvChoice(Base):
    __tablename__ = "adv_choices"

    id: Mapped[str] = mapped_column(VARCHAR(26), primary_key=True, index=True, default=generate_ulid)
    source_dialogue_line_id: Mapped[str] = mapped_column(ForeignKey("adv_dialogue_lines.id"), nullable=False) # The dialogue line that presents this choice
    text: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    next_dialogue_line_id: Mapped[str] = mapped_column(ForeignKey("adv_dialogue_lines.id"), nullable=False) # The dialogue line this choice leads to
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    source_dialogue_line: Mapped["AdvDialogueLine"] = relationship(back_populates="choices_offered", foreign_keys=[source_dialogue_line_id])
    next_dialogue_line: Mapped["AdvDialogueLine"] = relationship(foreign_keys=[next_dialogue_line_id])
