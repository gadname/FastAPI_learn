import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.main import app as fastapi_app_instance # Aliased import for clarity
from app.db.database import Base, get_db_sync # Import base and original get_db_sync
# Import all relevant models used in fixtures or tests
from app.models.adv_character import AdvCharacter
from app.models.adv_scenario import AdvScenario
from app.models.adv_dialogue import AdvDialogueLine, AdvChoice
from app.models.adv_session import AdvChatSession


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:" # In-memory SQLite for tests

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # check_same_thread for SQLite
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Apply model definitions to the test database ONCE for the engine.
# Individual tests will then manage table data (create/drop data or tables per test).
# Base.metadata.create_all(bind=engine) # This can be done here or in session-scoped fixtures more granularly

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=engine) # Create tables at the beginning of each test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine) # Drop tables at the end of each test

@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    # This override applies for the whole module.
    # db_session fixture will ensure data isolation between tests.
    def override_get_db_sync_for_test():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    # Use pytest's monkeypatch fixture, passed as an argument to the client fixture
    # No, client fixture is module-scoped, monkeypatch is function-scoped by default.
    # Need to use monkeypatch.setattr directly or a module-scoped monkeypatch.
    # For simplicity, will try direct setattr on the imported app.main module's attributes.
    # This relies on app.main having already imported the engine names.

    import app.main # To allow patching its members
    import app.db.database # To access original engines if needed for restoration, though monkeypatch handles it

    # Define the test engines for patching
    from sqlalchemy.ext.asyncio import create_async_engine as actual_create_async_engine
    ASYNC_SQLITE_URL_FOR_PATCH = "sqlite+aiosqlite:///:memory:?cache=shared"
    test_async_engine_for_patch = actual_create_async_engine(ASYNC_SQLITE_URL_FOR_PATCH, connect_args={"check_same_thread": False})
    # 'engine' is the global sync SQLite engine for tests (from SQLALCHEMY_DATABASE_URL)
    test_sync_engine_for_patch = engine

    # Store original engines that app.main imported, to restore them
    original_app_main_async_engine = app.main.async_engine
    original_app_main_engine_sync = app.main.engine_sync

    # Patch the names in app.main's scope that startup event will use
    app.main.async_engine = test_async_engine_for_patch
    app.main.engine_sync = test_sync_engine_for_patch

    fastapi_app_instance.dependency_overrides[get_db_sync] = override_get_db_sync_for_test

    try:
        with TestClient(fastapi_app_instance) as c:
            yield c
    finally:
        # Restore original engines in app.main's scope
        app.main.async_engine = original_app_main_async_engine
        app.main.engine_sync = original_app_main_engine_sync
        # Clean up dependency overrides
        del fastapi_app_instance.dependency_overrides[get_db_sync]

# --- Data Fixtures ---
@pytest.fixture(scope="function")
def test_character_narrator(db_session: Session) -> AdvCharacter:
    char = AdvCharacter(name="Narrator")
    db_session.add(char)
    db_session.commit()
    db_session.refresh(char)
    return char

@pytest.fixture(scope="function")
def test_character_bot(db_session: Session) -> AdvCharacter:
    char = AdvCharacter(name="Assistant Bot")
    db_session.add(char)
    db_session.commit()
    db_session.refresh(char)
    return char

@pytest.fixture(scope="function")
def test_scenario1(db_session: Session, test_character_narrator: AdvCharacter, test_character_bot: AdvCharacter) -> AdvScenario:
    scenario = AdvScenario(name="Test Scenario 1", description="A simple test scenario.")
    db_session.add(scenario)
    db_session.commit()
    db_session.refresh(scenario)

    # Add dialogue lines
    # dl1 will now have a choice leading to dl2, as per test plan adjustment.
    dl1 = AdvDialogueLine(scenario_id=scenario.id, character_id=test_character_narrator.id, text="Welcome! Proceed to learn more?", order=1)
    dl2 = AdvDialogueLine(scenario_id=scenario.id, character_id=test_character_bot.id, text="How can I help you today?", order=2)
    dl3 = AdvDialogueLine(scenario_id=scenario.id, character_id=test_character_narrator.id, text="You chose to learn about A.", order=3) # Target for a choice from dl2
    dl4 = AdvDialogueLine(scenario_id=scenario.id, character_id=test_character_narrator.id, text="You chose to learn about B.", order=4) # Target for another choice from dl2

    db_session.add_all([dl1, dl2, dl3, dl4])
    db_session.commit() # Commit dialogues first to get IDs

    # Refresh to ensure IDs are populated before creating choices
    db_session.refresh(dl1)
    db_session.refresh(dl2)
    db_session.refresh(dl3)
    db_session.refresh(dl4)

    # Add a choice to dl1 leading to dl2
    choice_on_dl1 = AdvChoice(source_dialogue_line_id=dl1.id, text="Yes, proceed.", next_dialogue_line_id=dl2.id)
    db_session.add(choice_on_dl1)

    # Add choices to dl2
    choice1_on_dl2 = AdvChoice(source_dialogue_line_id=dl2.id, text="Tell me about A", next_dialogue_line_id=dl3.id)
    choice2_on_dl2 = AdvChoice(source_dialogue_line_id=dl2.id, text="Tell me about B", next_dialogue_line_id=dl4.id)
    db_session.add_all([choice1_on_dl2, choice2_on_dl2])

    # Set scenario's first dialogue line
    scenario.first_dialogue_line_id = dl1.id
    db_session.add(scenario) # Add scenario again to save first_dialogue_line_id

    db_session.commit() # Commit choices and scenario update

    # Refresh objects to pick up any relationship changes or DB-generated values
    db_session.refresh(scenario)
    db_session.refresh(dl1)
    db_session.refresh(dl2)
    # For dl1 and dl2, if 'choices_offered' relationship is used by tests directly after this fixture,
    # they might need specific refreshing or a new query if the session closes and reopens,
    # but for direct ID usage and service layer tests that re-fetch, this should be fine.

    return scenario
