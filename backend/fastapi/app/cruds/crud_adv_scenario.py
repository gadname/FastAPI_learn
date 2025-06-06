from sqlalchemy.orm import Session, joinedload
from app.models.adv_scenario import AdvScenario
from app.models.adv_dialogue import AdvDialogueLine # For joinedload path
from app.models.adv_character import AdvCharacter # For joinedload path
from app.models.adv_dialogue import AdvChoice # For joinedload path
from app.schemas.adv_chat import AdvScenarioCreate # Add AdvScenarioUpdate if needed for other fields

def create_adv_scenario(db: Session, scenario: AdvScenarioCreate) -> AdvScenario:
    db_scenario = AdvScenario(**scenario.model_dump(exclude_unset=True)) # exclude_unset for optional fields
    db.add(db_scenario)
    db.commit()
    db.refresh(db_scenario)
    return db_scenario

def get_adv_scenario(db: Session, scenario_id: str) -> AdvScenario | None:
    return db.query(AdvScenario).filter(AdvScenario.id == scenario_id).first()

def get_adv_scenarios(db: Session, skip: int = 0, limit: int = 100) -> list[AdvScenario]:
    return db.query(AdvScenario).offset(skip).limit(limit).all()

def get_adv_scenario_with_details(db: Session, scenario_id: str) -> AdvScenario | None:
    return (
        db.query(AdvScenario)
        .options(
            joinedload(AdvScenario.dialogue_lines)
            .options(
                joinedload(AdvDialogueLine.character), # AdvDialogueLine -> AdvCharacter
                joinedload(AdvDialogueLine.choices_offered) # AdvDialogueLine -> AdvChoice
            )
        )
        .filter(AdvScenario.id == scenario_id)
        .order_by(AdvDialogueLine.order) # Assuming AdvScenario.dialogue_lines is ordered by AdvDialogueLine.order
        .first()
    )

def update_adv_scenario_first_dialogue(db: Session, scenario_id: str, first_dialogue_line_id: str) -> AdvScenario | None:
    db_scenario = get_adv_scenario(db, scenario_id)
    if db_scenario:
        db_scenario.first_dialogue_line_id = first_dialogue_line_id
        db.commit()
        db.refresh(db_scenario)
    return db_scenario
