from sqlalchemy.orm import Session
from app.models.adv_session import AdvChatSession
from app.schemas.adv_chat import AdvChatSessionCreate
from datetime import datetime # Potentially for updated_at, though model might handle it

def create_adv_chat_session(db: Session, session_create: AdvChatSessionCreate, initial_dialogue_id: str) -> AdvChatSession:
    db_session = AdvChatSession(
        **session_create.model_dump(),
        current_dialogue_line_id=initial_dialogue_id
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_adv_chat_session(db: Session, session_id: str) -> AdvChatSession | None:
    return db.query(AdvChatSession).filter(AdvChatSession.id == session_id).first()

def update_adv_chat_session_current_dialogue(db: Session, session_id: str, new_dialogue_line_id: str) -> AdvChatSession | None:
    db_session = get_adv_chat_session(db, session_id)
    if db_session:
        db_session.current_dialogue_line_id = new_dialogue_line_id
        # db_session.updated_at = datetime.utcnow() # The model AdvChatSession has onupdate=datetime.utcnow for updated_at
        db.commit()
        db.refresh(db_session)
    return db_session
