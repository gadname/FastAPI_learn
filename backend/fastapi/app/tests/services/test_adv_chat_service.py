import pytest
from sqlalchemy.orm import Session
from app.services import adv_chat_service
# Schemas are not directly used for requests here, but good for reference
from app.schemas.adv_chat import StartChatRequest, MakeChoiceRequest
from app.models.adv_scenario import AdvScenario
from app.models.adv_character import AdvCharacter
from app.models.adv_dialogue import AdvDialogueLine, AdvChoice
from app.cruds import crud_adv_session # For manually updating session in one test
from fastapi import HTTPException

def test_start_new_adv_session(db_session: Session, test_scenario1: AdvScenario):
    scenario_id = test_scenario1.id
    chat_state = adv_chat_service.start_new_adv_session(db=db_session, scenario_id=scenario_id)

    assert chat_state is not None
    assert chat_state.scenario_name == test_scenario1.name
    # According to updated test_scenario1, dl1 is "Welcome! Proceed to learn more?" by Narrator
    assert chat_state.current_dialogue.text == "Welcome! Proceed to learn more?"
    assert chat_state.current_dialogue.character.name == "Narrator"
    # dl1 now has one choice leading to dl2
    assert len(chat_state.current_dialogue.choices_offered) == 1
    assert chat_state.current_dialogue.choices_offered[0].text == "Yes, proceed."
    assert not chat_state.is_end_of_scenario

def test_get_current_chat_state(db_session: Session, test_scenario1: AdvScenario):
    # Start a session first
    session_state = adv_chat_service.start_new_adv_session(db=db_session, scenario_id=test_scenario1.id)

    retrieved_state = adv_chat_service.get_current_chat_state(db=db_session, session_id=session_state.session_id)
    assert retrieved_state is not None
    assert retrieved_state.session_id == session_state.session_id
    assert retrieved_state.current_dialogue.id == session_state.current_dialogue.id
    assert retrieved_state.scenario_name == test_scenario1.name

def test_process_user_choice(db_session: Session, test_scenario1: AdvScenario):
    # Start session. Based on updated test_scenario1, current dialogue is dl1 ("Welcome! Proceed...?"), which has one choice to dl2.
    chat_state = adv_chat_service.start_new_adv_session(db=db_session, scenario_id=test_scenario1.id)

    assert chat_state.current_dialogue.text == "Welcome! Proceed to learn more?"
    assert len(chat_state.current_dialogue.choices_offered) == 1

    choice_to_dl2 = chat_state.current_dialogue.choices_offered[0]
    assert choice_to_dl2.text == "Yes, proceed."

    # Make the choice to go to dl2
    next_chat_state = adv_chat_service.process_user_choice(
        db=db_session, session_id=chat_state.session_id, choice_id=choice_to_dl2.id
    )

    assert next_chat_state is not None
    # dl2 text is "How can I help you today?"
    assert next_chat_state.current_dialogue.text == "How can I help you today?"
    assert next_chat_state.current_dialogue.character.name == "Assistant Bot"
    # dl2 has two choices ("Tell me about A", "Tell me about B")
    assert len(next_chat_state.current_dialogue.choices_offered) == 2
    assert not next_chat_state.is_end_of_scenario

    # Make another choice (from dl2 to dl3)
    choice_to_dl3 = next_chat_state.current_dialogue.choices_offered[0] # "Tell me about A"
    final_chat_state = adv_chat_service.process_user_choice(
        db=db_session, session_id=next_chat_state.session_id, choice_id=choice_to_dl3.id
    )

    assert final_chat_state is not None
    # dl3 text is "You chose to learn about A."
    assert final_chat_state.current_dialogue.text == "You chose to learn about A."
    assert not final_chat_state.current_dialogue.choices_offered # dl3 has no choices
    assert final_chat_state.is_end_of_scenario # No choices offered = end

def test_start_session_scenario_not_found(db_session: Session):
    with pytest.raises(HTTPException) as excinfo:
        adv_chat_service.start_new_adv_session(db=db_session, scenario_id="non_existent_scenario_id")
    assert excinfo.value.status_code == 404
    assert "Scenario not found" in excinfo.value.detail

def test_process_choice_invalid_choice_for_dialogue(db_session: Session, test_scenario1: AdvScenario):
    # Start session. On dl1.
    chat_state = adv_chat_service.start_new_adv_session(db=db_session, scenario_id=test_scenario1.id)

    # Get a choice that is NOT from dl1. E.g., a choice from dl2.
    dl2 = db_session.query(AdvDialogueLine).filter(AdvDialogueLine.scenario_id == test_scenario1.id, AdvDialogueLine.order == 2).first()
    assert dl2 is not None
    choice_from_dl2 = db_session.query(AdvChoice).filter(AdvChoice.source_dialogue_line_id == dl2.id).first()
    assert choice_from_dl2 is not None # Ensure dl2 has choices as per fixture

    with pytest.raises(HTTPException) as excinfo:
        adv_chat_service.process_user_choice(db_session, session_id=chat_state.session_id, choice_id=choice_from_dl2.id)
    assert excinfo.value.status_code == 400
    assert "Invalid choice for the current dialogue" in excinfo.value.detail

def test_process_choice_session_not_found(db_session: Session, test_scenario1: AdvScenario):
    # Need a valid choice_id from the fixture for this test
    dl1 = db_session.query(AdvDialogueLine).filter(AdvDialogueLine.scenario_id == test_scenario1.id, AdvDialogueLine.order == 1).first()
    choice_on_dl1 = db_session.query(AdvChoice).filter(AdvChoice.source_dialogue_line_id == dl1.id).first()
    assert choice_on_dl1 is not None

    with pytest.raises(HTTPException) as excinfo:
        adv_chat_service.process_user_choice(db_session, session_id="non_existent_session_id", choice_id=choice_on_dl1.id)
    assert excinfo.value.status_code == 404
    assert "Chat session not found" in excinfo.value.detail

def test_process_choice_choice_not_found(db_session: Session, test_scenario1: AdvScenario):
    chat_state = adv_chat_service.start_new_adv_session(db=db_session, scenario_id=test_scenario1.id)
    with pytest.raises(HTTPException) as excinfo:
        adv_chat_service.process_user_choice(db_session, session_id=chat_state.session_id, choice_id="non_existent_choice_id")
    assert excinfo.value.status_code == 404
    assert "Choice not found" in excinfo.value.detail
