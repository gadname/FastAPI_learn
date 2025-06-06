from __future__ import annotations # Enables postponed evaluation of annotations
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# --- Character Schemas ---
class AdvCharacterBase(BaseModel):
    name: str

class AdvCharacterCreate(AdvCharacterBase):
    pass

class AdvCharacterResponse(AdvCharacterBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Choice Schemas ---
class AdvChoiceBase(BaseModel):
    text: str
    next_dialogue_line_id: str

class AdvChoiceCreate(AdvChoiceBase):
    pass

class AdvChoiceResponse(AdvChoiceBase):
    id: str
    source_dialogue_line_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Dialogue Line Schemas ---
class AdvDialogueLineBase(BaseModel):
    text: str
    character_id: Optional[str] = None
    order: int
    emotion: Optional[str] = None
    pose: Optional[str] = None

class AdvDialogueLineCreate(AdvDialogueLineBase):
    # choices: List[AdvChoiceCreate] = [] # If creating choices inline
    pass

class AdvDialogueLineResponse(AdvDialogueLineBase):
    id: str
    scenario_id: str
    character: Optional[AdvCharacterResponse] = None
    choices_offered: List[AdvChoiceResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Scenario Schemas ---
class AdvScenarioBase(BaseModel):
    name: str
    description: Optional[str] = None

class AdvScenarioCreate(AdvScenarioBase):
    # dialogue_lines: List[AdvDialogueLineCreate] = [] # If creating dialogues inline
    first_dialogue_line_id: Optional[str] = None
    pass

class AdvScenarioResponse(AdvScenarioBase):
    id: str
    created_at: datetime
    updated_at: datetime
    first_dialogue_line_id: Optional[str] = None

    class Config:
        from_attributes = True

class AdvScenarioDetailResponse(AdvScenarioResponse):
    dialogue_lines: List[AdvDialogueLineResponse] = []

# --- Chat Session Schemas ---
class AdvChatSessionBase(BaseModel):
    scenario_id: str

class AdvChatSessionCreate(AdvChatSessionBase):
    # current_dialogue_line_id: Optional[str] = None # Set by service
    pass

class AdvChatSessionResponse(AdvChatSessionBase):
    id: str
    current_dialogue_line_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- API Request/Response Schemas ---
class StartChatRequest(BaseModel):
    scenario_id: str

class MakeChoiceRequest(BaseModel):
    choice_id: str # This is AdvChoice.id

class ChatStateResponse(BaseModel):
    session_id: str
    current_dialogue: AdvDialogueLineResponse
    # available_choices are in current_dialogue.choices_offered, so removed redundant field
    scenario_name: str
    is_end_of_scenario: bool = False

# Pydantic v2 generally handles forward references automatically within the same module.
# If using Pydantic v1 or for explicit updates if models were defined in a different order or split into files:
# AdvDialogueLineResponse.update_forward_refs()
# AdvScenarioDetailResponse.update_forward_refs()
# However, with from __future__ import annotations and definitions in this order,
# explicit calls to update_forward_refs or model_rebuild should not be necessary.
