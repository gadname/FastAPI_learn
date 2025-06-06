from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db_sync # Use the synchronous session
from app.schemas import adv_chat as adv_schemas # Use alias for clarity
from app.services import adv_chat_service
from app.cruds import crud_adv_scenario, crud_adv_character, crud_adv_dialogue
from typing import List

router = APIRouter(
    prefix="/adv-chat",
    tags=["ADV Chat"],
)

# Scenario Endpoints
@router.post("/scenarios", response_model=adv_schemas.AdvScenarioResponse)
def create_scenario(
    scenario: adv_schemas.AdvScenarioCreate, db: Session = Depends(get_db_sync)
):
    return crud_adv_scenario.create_adv_scenario(db=db, scenario=scenario)

@router.get("/scenarios", response_model=List[adv_schemas.AdvScenarioResponse])
def list_scenarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_sync)):
    scenarios = crud_adv_scenario.get_adv_scenarios(db=db, skip=skip, limit=limit)
    return scenarios

@router.get("/scenarios/{scenario_id}", response_model=adv_schemas.AdvScenarioDetailResponse)
def get_scenario_details(scenario_id: str, db: Session = Depends(get_db_sync)):
    db_scenario = crud_adv_scenario.get_adv_scenario_with_details(db, scenario_id=scenario_id)
    if not db_scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    dialogue_responses = []
    if db_scenario.dialogue_lines: # Ensure there are dialogue lines
        for dl in db_scenario.dialogue_lines:
            char_resp = adv_schemas.AdvCharacterResponse.model_validate(dl.character) if dl.character else None
            choice_resps = [adv_schemas.AdvChoiceResponse.model_validate(ch) for ch in dl.choices_offered] if dl.choices_offered else []
            dialogue_responses.append(
                adv_schemas.AdvDialogueLineResponse(
                    id=dl.id, text=dl.text, character_id=dl.character_id, order=dl.order,
                    emotion=dl.emotion, pose=dl.pose, scenario_id=dl.scenario_id,
                    character=char_resp, choices_offered=choice_resps,
                    created_at=dl.created_at, updated_at=dl.updated_at
                )
            )

    return adv_schemas.AdvScenarioDetailResponse(
        id=db_scenario.id, name=db_scenario.name, description=db_scenario.description,
        created_at=db_scenario.created_at, updated_at=db_scenario.updated_at,
        first_dialogue_line_id=db_scenario.first_dialogue_line_id,
        dialogue_lines=dialogue_responses
    )

@router.post("/scenarios/{scenario_id}/dialogue-lines", response_model=adv_schemas.AdvDialogueLineResponse)
def create_dialogue_line_for_scenario(
    scenario_id: str, dialogue_line: adv_schemas.AdvDialogueLineCreate, db: Session = Depends(get_db_sync)
):
    db_scenario = crud_adv_scenario.get_adv_scenario(db, scenario_id=scenario_id)
    if not db_scenario:
        raise HTTPException(status_code=404, detail="Scenario not found for dialogue line creation")

    created_line_orm = crud_adv_dialogue.create_adv_dialogue_line(db=db, dialogue_line=dialogue_line, scenario_id=scenario_id)

    if not db_scenario.first_dialogue_line_id:
        all_lines = crud_adv_dialogue.get_adv_dialogue_lines_for_scenario(db, scenario_id=scenario_id)
        if all_lines and created_line_orm.id == min(all_lines, key=lambda x: x.order).id:
            crud_adv_scenario.update_adv_scenario_first_dialogue(db, scenario_id=scenario_id, first_dialogue_line_id=created_line_orm.id)

    db_line_with_relations = crud_adv_dialogue.get_adv_dialogue_line(db, created_line_orm.id)
    if not db_line_with_relations:
         raise HTTPException(status_code=500, detail="Failed to fetch created dialogue line with relations")

    char_resp = adv_schemas.AdvCharacterResponse.model_validate(db_line_with_relations.character) if db_line_with_relations.character else None
    choices_resp = [adv_schemas.AdvChoiceResponse.model_validate(ch) for ch in db_line_with_relations.choices_offered] if db_line_with_relations.choices_offered else []

    return adv_schemas.AdvDialogueLineResponse(
        id=db_line_with_relations.id, text=db_line_with_relations.text, character_id=db_line_with_relations.character_id,
        order=db_line_with_relations.order, emotion=db_line_with_relations.emotion, pose=db_line_with_relations.pose,
        scenario_id=db_line_with_relations.scenario_id, character=char_resp, choices_offered=choices_resp,
        created_at=db_line_with_relations.created_at,updated_at=db_line_with_relations.updated_at
    )

@router.post("/dialogue-lines/{dialogue_line_id}/choices", response_model=adv_schemas.AdvChoiceResponse)
def create_choice_for_dialogue_line(
    dialogue_line_id: str, choice: adv_schemas.AdvChoiceCreate, db: Session = Depends(get_db_sync)
):
    db_dialogue_line = crud_adv_dialogue.get_adv_dialogue_line(db, dialogue_line_id=dialogue_line_id)
    if not db_dialogue_line:
        raise HTTPException(status_code=404, detail="Source dialogue line not found for choice creation")

    db_next_dialogue_line = crud_adv_dialogue.get_adv_dialogue_line(db, dialogue_line_id=choice.next_dialogue_line_id)
    if not db_next_dialogue_line:
        raise HTTPException(status_code=404, detail="Next dialogue line specified in choice not found")

    return crud_adv_dialogue.create_adv_choice(db=db, choice=choice, source_dialogue_line_id=dialogue_line_id)

# Character Endpoint
@router.post("/characters", response_model=adv_schemas.AdvCharacterResponse)
def create_character(
    character: adv_schemas.AdvCharacterCreate, db: Session = Depends(get_db_sync)
):
    db_character = crud_adv_character.get_adv_character_by_name(db, name=character.name)
    if db_character:
        raise HTTPException(status_code=400, detail="Character name already registered")
    return crud_adv_character.create_adv_character(db=db, character=character)

# Chat Session Endpoints
@router.post("/sessions/start", response_model=adv_schemas.ChatStateResponse)
def start_chat_session(
    start_request: adv_schemas.StartChatRequest, db: Session = Depends(get_db_sync)
):
    try:
        return adv_chat_service.start_new_adv_session(db=db, scenario_id=start_request.scenario_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        # TODO: Log the error e
        print(f"Unexpected error in start_chat_session: {e}") # Basic logging
        raise HTTPException(status_code=500, detail="Internal server error starting chat session")

@router.get("/sessions/{session_id}", response_model=adv_schemas.ChatStateResponse)
def get_session_state(session_id: str, db: Session = Depends(get_db_sync)):
    try:
        return adv_chat_service.get_current_chat_state(db=db, session_id=session_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        # TODO: Log the error e
        print(f"Unexpected error in get_session_state: {e}") # Basic logging
        raise HTTPException(status_code=500, detail="Internal server error retrieving chat state")

@router.post("/sessions/{session_id}/choice", response_model=adv_schemas.ChatStateResponse)
def make_choice_in_session(
    session_id: str, choice_request: adv_schemas.MakeChoiceRequest, db: Session = Depends(get_db_sync)
):
    try:
        return adv_chat_service.process_user_choice(
            db=db, session_id=session_id, choice_id=choice_request.choice_id
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        # TODO: Log the error e
        print(f"Unexpected error in make_choice_in_session: {e}") # Basic logging
        raise HTTPException(status_code=500, detail="Internal server error processing choice")
