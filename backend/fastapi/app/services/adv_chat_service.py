from sqlalchemy.orm import Session
from app.cruds import crud_adv_scenario, crud_adv_session, crud_adv_dialogue
from app.models.adv_scenario import AdvScenario # For type hinting
from app.models.adv_session import AdvChatSession # For type hinting
from app.models.adv_dialogue import AdvDialogueLine, AdvChoice # For type hinting
from app.schemas.adv_chat import (
    AdvChatSessionCreate,
    ChatStateResponse,
    AdvDialogueLineResponse,
    AdvCharacterResponse,
    AdvChoiceResponse
)
from fastapi import HTTPException

def get_current_chat_state(db: Session, session_id: str) -> ChatStateResponse:
    # 1. Fetch the session
    db_session: AdvChatSession | None = crud_adv_session.get_adv_chat_session(db, session_id=session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Chat session not found")

    # 2. Fetch the current dialogue line with its character and choices
    # The CRUD function get_adv_dialogue_line is expected to use joinedload for character and choices_offered
    current_dialogue: AdvDialogueLine | None = crud_adv_dialogue.get_adv_dialogue_line(db, dialogue_line_id=db_session.current_dialogue_line_id)
    if not current_dialogue:
        # This case should ideally not happen if session integrity and dialogue data are maintained
        raise HTTPException(status_code=404, detail="Current dialogue line not found for session.")

    # 3. Fetch scenario for context (name)
    db_scenario: AdvScenario | None = crud_adv_scenario.get_adv_scenario(db, scenario_id=db_session.scenario_id)
    if not db_scenario:
        # This case should ideally not happen if session integrity and scenario data are maintained
        raise HTTPException(status_code=404, detail="Scenario not found for session.")

    # 4. Prepare AdvDialogueLineResponse
    character_response = None
    if current_dialogue.character: # Character is eagerly loaded by crud_adv_dialogue.get_adv_dialogue_line
        character_response = AdvCharacterResponse.model_validate(current_dialogue.character)

    # Choices are eagerly loaded by crud_adv_dialogue.get_adv_dialogue_line
    choices_response = [AdvChoiceResponse.model_validate(choice) for choice in current_dialogue.choices_offered]

    dialogue_response = AdvDialogueLineResponse(
        id=current_dialogue.id,
        text=current_dialogue.text,
        character_id=current_dialogue.character_id,
        order=current_dialogue.order,
        emotion=current_dialogue.emotion,
        pose=current_dialogue.pose,
        scenario_id=current_dialogue.scenario_id,
        character=character_response,
        choices_offered=choices_response,
        created_at=current_dialogue.created_at,
        updated_at=current_dialogue.updated_at
    )

    is_end = not bool(current_dialogue.choices_offered)

    return ChatStateResponse(
        session_id=db_session.id,
        current_dialogue=dialogue_response,
        scenario_name=db_scenario.name,
        is_end_of_scenario=is_end
    )

def start_new_adv_session(db: Session, scenario_id: str) -> ChatStateResponse:
    # 1. Fetch the scenario
    db_scenario: AdvScenario | None = crud_adv_scenario.get_adv_scenario(db, scenario_id=scenario_id)
    if not db_scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    # 2. Determine the first dialogue line
    first_dialogue_line: AdvDialogueLine | None = None
    if db_scenario.first_dialogue_line_id:
        # get_adv_dialogue_line loads relations needed for ChatStateResponse
        first_dialogue_line = crud_adv_dialogue.get_adv_dialogue_line(db, dialogue_line_id=db_scenario.first_dialogue_line_id)

    if not first_dialogue_line:
        # Fallback: Get dialogue lines for the scenario, ordered by 'order'
        dialogue_lines = crud_adv_dialogue.get_adv_dialogue_lines_for_scenario(db, scenario_id=scenario_id)
        if not dialogue_lines:
            raise HTTPException(status_code=404, detail="Scenario has no dialogue lines")

        # The first element is the one with the smallest order.
        # Re-fetch it using get_adv_dialogue_line to ensure all relations (character, choices) are loaded.
        first_dialogue_line = crud_adv_dialogue.get_adv_dialogue_line(db, dialogue_line_id=dialogue_lines[0].id)

    if not first_dialogue_line:
             # This would imply the dialogue line (either from first_dialogue_line_id or from list) was deleted
             # or couldn't be loaded with its relations.
             raise HTTPException(status_code=404, detail="Could not determine or fully load the first dialogue line for the scenario.")

    # 3. Create the chat session
    session_create = AdvChatSessionCreate(scenario_id=scenario_id)
    db_session: AdvChatSession = crud_adv_session.create_adv_chat_session(
        db, session_create=session_create, initial_dialogue_id=first_dialogue_line.id
    )

    # 4. Return the initial chat state
    return get_current_chat_state(db, session_id=db_session.id)

def process_user_choice(db: Session, session_id: str, choice_id: str) -> ChatStateResponse:
    # 1. Fetch the session
    db_session: AdvChatSession | None = crud_adv_session.get_adv_chat_session(db, session_id=session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Chat session not found")

    # 2. Validate the choice
    #   a. Fetch the choice details
    db_choice: AdvChoice | None = crud_adv_dialogue.get_adv_choice(db, choice_id=choice_id)
    if not db_choice:
        raise HTTPException(status_code=404, detail="Choice not found")
    #   b. Ensure the choice belongs to the current dialogue line of the session
    if db_choice.source_dialogue_line_id != db_session.current_dialogue_line_id:
        raise HTTPException(status_code=400, detail="Invalid choice for the current dialogue.")

    # 3. Update the session's current dialogue line to the one indicated by the choice
    # Ensure the target dialogue line exists before updating.
    next_dialogue_line: AdvDialogueLine | None = crud_adv_dialogue.get_adv_dialogue_line(db, dialogue_line_id=db_choice.next_dialogue_line_id)
    if not next_dialogue_line:
        # This implies an orphaned choice, pointing to a non-existent dialogue line.
        raise HTTPException(status_code=404, detail="The dialogue line this choice leads to was not found.")

    updated_session = crud_adv_session.update_adv_chat_session_current_dialogue(
        db, session_id=session_id, new_dialogue_line_id=db_choice.next_dialogue_line_id
    )
    # This update_adv_chat_session_current_dialogue already checks if db_session exists.
    # If it returns None here, it means the session disappeared or another issue occurred.
    if not updated_session:
        raise HTTPException(status_code=500, detail="Failed to update session state after validating choice.")

    # 4. Return the new chat state
    return get_current_chat_state(db, session_id=session_id)
