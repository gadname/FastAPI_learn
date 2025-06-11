from sqlalchemy.orm import Session, joinedload
from app.models.adv_dialogue import AdvDialogueLine, AdvChoice
from app.models.adv_character import AdvCharacter # For joinedload path
from app.schemas.adv_chat import AdvDialogueLineCreate, AdvChoiceCreate

# AdvDialogueLine CRUD
def create_adv_dialogue_line(db: Session, dialogue_line: AdvDialogueLineCreate, scenario_id: str) -> AdvDialogueLine:
    db_dialogue_line = AdvDialogueLine(**dialogue_line.model_dump(), scenario_id=scenario_id)
    db.add(db_dialogue_line)
    db.commit()
    db.refresh(db_dialogue_line)
    return db_dialogue_line

def get_adv_dialogue_line(db: Session, dialogue_line_id: str) -> AdvDialogueLine | None:
    return (
        db.query(AdvDialogueLine)
        .options(
            joinedload(AdvDialogueLine.character),      # Eager load character
            joinedload(AdvDialogueLine.choices_offered) # Eager load choices offered
        )
        .filter(AdvDialogueLine.id == dialogue_line_id)
        .first()
    )

def get_adv_dialogue_lines_for_scenario(db: Session, scenario_id: str) -> list[AdvDialogueLine]:
    return (
        db.query(AdvDialogueLine)
        .filter(AdvDialogueLine.scenario_id == scenario_id)
        .order_by(AdvDialogueLine.order)
        .all()
    )

# AdvChoice CRUD
def create_adv_choice(db: Session, choice: AdvChoiceCreate, source_dialogue_line_id: str) -> AdvChoice:
    # Ensure the next_dialogue_line_id exists if you want to add validation here,
    # though referential integrity at DB level should handle it.
    # Also ensure source_dialogue_line_id exists.
    db_choice = AdvChoice(**choice.model_dump(), source_dialogue_line_id=source_dialogue_line_id)
    db.add(db_choice)
    db.commit()
    db.refresh(db_choice)
    return db_choice

def get_adv_choice(db: Session, choice_id: str) -> AdvChoice | None:
    return db.query(AdvChoice).filter(AdvChoice.id == choice_id).first()

def get_adv_choices_for_dialogue_line(db: Session, dialogue_line_id: str) -> list[AdvChoice]:
    return (
        db.query(AdvChoice)
        .filter(AdvChoice.source_dialogue_line_id == dialogue_line_id)
        .all()
    )
