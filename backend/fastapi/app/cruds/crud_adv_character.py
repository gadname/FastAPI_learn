from sqlalchemy.orm import Session
from app.models.adv_character import AdvCharacter
from app.schemas.adv_chat import AdvCharacterCreate # AdvCharacterUpdate not used for now

def create_adv_character(db: Session, character: AdvCharacterCreate) -> AdvCharacter:
    db_character = AdvCharacter(**character.model_dump())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character

def get_adv_character(db: Session, character_id: str) -> AdvCharacter | None:
    return db.query(AdvCharacter).filter(AdvCharacter.id == character_id).first()

def get_adv_character_by_name(db: Session, name: str) -> AdvCharacter | None:
    return db.query(AdvCharacter).filter(AdvCharacter.name == name).first()

def get_adv_characters(db: Session, skip: int = 0, limit: int = 100) -> list[AdvCharacter]:
    return db.query(AdvCharacter).offset(skip).limit(limit).all()

# Update and delete functions can be added later if needed.
# For example:
# from app.schemas.adv_chat import AdvCharacterUpdate # Assuming this schema exists
# def update_adv_character(db: Session, character_id: str, character_update: AdvCharacterUpdate) -> AdvCharacter | None:
#     db_character = get_adv_character(db, character_id)
#     if db_character:
#         update_data = character_update.model_dump(exclude_unset=True)
#         for key, value in update_data.items():
#             setattr(db_character, key, value)
#         db.commit()
#         db.refresh(db_character)
#     return db_character

# def delete_adv_character(db: Session, character_id: str) -> AdvCharacter | None:
#     db_character = get_adv_character(db, character_id)
#     if db_character:
#         db.delete(db_character)
#         db.commit()
#     return db_character
