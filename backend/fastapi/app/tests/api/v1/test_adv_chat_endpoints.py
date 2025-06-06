from fastapi.testclient import TestClient
from sqlalchemy.orm import Session # For type hinting if using db_session fixture directly for setup/assertions
from app.schemas import adv_chat as adv_schemas
from app.models.adv_scenario import AdvScenario # For type hinting test_scenario1 fixture
from app.models.adv_character import AdvCharacter # For type hinting character fixtures

# Test Character Creation
def test_create_character_api(client: TestClient):
    response = client.post("/api/v1/adv-chat/characters", json={"name": "Unique New API Character"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Unique New API Character"
    assert "id" in data

    # Test duplicate name
    response = client.post("/api/v1/adv-chat/characters", json={"name": "Unique New API Character"})
    assert response.status_code == 400, response.text
    assert "Character name already registered" in response.json()["detail"]

# Test Scenario Creation & Retrieval
def test_create_and_get_scenario_api(client: TestClient):
    # Create Scenario
    scenario_data = {"name": "API Test Scenario Full", "description": "Created via API for full test"}
    response = client.post("/api/v1/adv-chat/scenarios", json=scenario_data)
    assert response.status_code == 200, response.text
    created_scenario = response.json()
    assert created_scenario["name"] == scenario_data["name"]
    scenario_id = created_scenario["id"]

    # Get Scenario Details
    response = client.get(f"/api/v1/adv-chat/scenarios/{scenario_id}")
    assert response.status_code == 200, response.text
    details = response.json()
    assert details["id"] == scenario_id
    assert details["name"] == scenario_data["name"]
    assert details["dialogue_lines"] == [] # Initially no dialogues

    # List Scenarios
    response = client.get("/api/v1/adv-chat/scenarios")
    assert response.status_code == 200, response.text
    # Ensure the created scenario is in the list
    assert any(sc["id"] == scenario_id for sc in response.json())


# Test Dialogue and Choice Creation for Scenario
def test_create_dialogue_and_choice_api(client: TestClient, test_character_bot: AdvCharacter):
    # 1. Create a scenario shell
    scenario_resp = client.post("/api/v1/adv-chat/scenarios", json={"name": "Scenario For Dialogues API", "description": "Test dialogues and choices"})
    assert scenario_resp.status_code == 200, scenario_resp.text
    scenario_id = scenario_resp.json()["id"]

    # 2. Create dialogue line 1
    dl1_data = {"text": "Hello from API DL1", "order": 1, "character_id": test_character_bot.id}
    dl1_resp = client.post(f"/api/v1/adv-chat/scenarios/{scenario_id}/dialogue-lines", json=dl1_data)
    assert dl1_resp.status_code == 200, dl1_resp.text
    dl1_id = dl1_resp.json()["id"]
    assert dl1_resp.json()["text"] == dl1_data["text"]
    assert dl1_resp.json()["character"]["id"] == test_character_bot.id

    # 3. Create dialogue line 2 (target for choice)
    dl2_data = {"text": "This is the target of a choice from API", "order": 2, "character_id": test_character_bot.id}
    dl2_resp = client.post(f"/api/v1/adv-chat/scenarios/{scenario_id}/dialogue-lines", json=dl2_data)
    assert dl2_resp.status_code == 200, dl2_resp.text
    dl2_id = dl2_resp.json()["id"]

    # 4. Create a choice for dialogue line 1, pointing to dialogue line 2
    choice_data = {"text": "Go to DL2 via API", "next_dialogue_line_id": dl2_id}
    choice_resp = client.post(f"/api/v1/adv-chat/dialogue-lines/{dl1_id}/choices", json=choice_data)
    assert choice_resp.status_code == 200, choice_resp.text
    assert choice_resp.json()["text"] == choice_data["text"]
    assert choice_resp.json()["next_dialogue_line_id"] == dl2_id

    # Verify scenario first_dialogue_line_id was updated
    scenario_details_resp = client.get(f"/api/v1/adv-chat/scenarios/{scenario_id}")
    assert scenario_details_resp.status_code == 200, scenario_details_resp.text
    assert scenario_details_resp.json()["first_dialogue_line_id"] == dl1_id


# Test Chat Session Flow via API
def test_chat_session_flow_api(client: TestClient, test_scenario1: AdvScenario):
    scenario_id = test_scenario1.id

    # Start session
    response = client.post("/api/v1/adv-chat/sessions/start", json={"scenario_id": scenario_id})
    assert response.status_code == 200, response.text
    chat_state = response.json()
    session_id = chat_state["session_id"]
    assert chat_state["scenario_name"] == test_scenario1.name
    # Based on updated test_scenario1 fixture, first line is "Welcome! Proceed to learn more?"
    assert chat_state["current_dialogue"]["text"] == "Welcome! Proceed to learn more?"
    assert len(chat_state["current_dialogue"]["choices_offered"]) == 1 # dl1 has one choice to dl2

    # Get current state (should be the same)
    response = client.get(f"/api/v1/adv-chat/sessions/{session_id}")
    assert response.status_code == 200, response.text
    assert response.json()["current_dialogue"]["text"] == "Welcome! Proceed to learn more?"

    # Make the choice from dl1 to dl2
    choice_to_dl2_id = chat_state["current_dialogue"]["choices_offered"][0]["id"]
    response = client.post(f"/api/v1/adv-chat/sessions/{session_id}/choice", json={"choice_id": choice_to_dl2_id})
    assert response.status_code == 200, response.text
    chat_state_after_first_choice = response.json()

    # Now on dl2: "How can I help you today?"
    assert chat_state_after_first_choice["current_dialogue"]["text"] == "How can I help you today?"
    assert len(chat_state_after_first_choice["current_dialogue"]["choices_offered"]) == 2 # dl2 has two choices

    # Make another choice (from dl2 to dl3: "Tell me about A")
    choice_to_dl3_id = chat_state_after_first_choice["current_dialogue"]["choices_offered"][0]["id"]
    response = client.post(f"/api/v1/adv-chat/sessions/{session_id}/choice", json={"choice_id": choice_to_dl3_id})
    assert response.status_code == 200, response.text
    chat_state_on_dl3 = response.json()

    # Now on dl3: "You chose to learn about A."
    assert chat_state_on_dl3["current_dialogue"]["text"] == "You chose to learn about A."
    assert len(chat_state_on_dl3["current_dialogue"]["choices_offered"]) == 0 # dl3 has no choices
    assert chat_state_on_dl3["is_end_of_scenario"] == True


def test_start_chat_scenario_not_found_api(client: TestClient):
    response = client.post("/api/v1/adv-chat/sessions/start", json={"scenario_id": "non_existent_api_scenario"})
    assert response.status_code == 404, response.text
    assert "Scenario not found" in response.json()["detail"]

def test_get_session_state_not_found_api(client: TestClient):
    response = client.get("/api/v1/adv-chat/sessions/non_existent_session_id")
    assert response.status_code == 404, response.text
    assert "Chat session not found" in response.json()["detail"]

def test_make_choice_session_not_found_api(client: TestClient):
    response = client.post("/api/v1/adv-chat/sessions/non_existent_session/choice", json={"choice_id": "any_choice"})
    assert response.status_code == 404, response.text
    assert "Chat session not found" in response.json()["detail"]

def test_make_choice_choice_not_found_api(client: TestClient, test_scenario1: AdvScenario):
    # Start a session
    start_resp = client.post("/api/v1/adv-chat/sessions/start", json={"scenario_id": test_scenario1.id})
    session_id = start_resp.json()["session_id"]

    response = client.post(f"/api/v1/adv-chat/sessions/{session_id}/choice", json={"choice_id": "non_existent_choice"})
    assert response.status_code == 404, response.text
    assert "Choice not found" in response.json()["detail"]

def test_make_choice_invalid_for_dialogue_api(client: TestClient, db_session: Session, test_scenario1: AdvScenario):
    # Start a session, it will be on dl1
    start_resp = client.post("/api/v1/adv-chat/sessions/start", json={"scenario_id": test_scenario1.id})
    session_id = start_resp.json()["session_id"]

    # Get a choice from dl2 (which is not the current dialogue line)
    dl2_orm = db_session.query(AdvDialogueLine).filter(AdvDialogueLine.scenario_id == test_scenario1.id, AdvDialogueLine.order == 2).first()
    choice_from_dl2_orm = db_session.query(AdvChoice).filter(AdvChoice.source_dialogue_line_id == dl2_orm.id).first()
    assert choice_from_dl2_orm is not None

    response = client.post(f"/api/v1/adv-chat/sessions/{session_id}/choice", json={"choice_id": choice_from_dl2_orm.id})
    assert response.status_code == 400, response.text # Bad Request
    assert "Invalid choice for the current dialogue" in response.json()["detail"]
