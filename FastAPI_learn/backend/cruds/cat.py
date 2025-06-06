from typing import List, Optional
from sqlalchemy.orm import Session
from models.cat import Cat
from schemas.cat import CatCreate, CatUpdate

def get_cat(db: Session, cat_id: int) -> Optional[Cat]:
    return db.query(Cat).filter(Cat.id == cat_id).first()

def get_cats(db: Session, skip: int = 0, limit: int = 100) -> List[Cat]:
    return db.query(Cat).offset(skip).limit(limit).all()

def create_cat(db: Session, cat: CatCreate) -> Cat:
    db_cat = Cat(**cat.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def update_cat(db: Session, cat_id: int, cat: CatUpdate) -> Optional[Cat]:
    db_cat = get_cat(db, cat_id)
    if not db_cat:
        return None
    
    update_data = cat.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_cat, field, value)
    
    db.commit()
    db.refresh(db_cat)
    return db_cat

def delete_cat(db: Session, cat_id: int) -> bool:
    db_cat = get_cat(db, cat_id)
    if not db_cat:
        return False
    
    db.delete(db_cat)
    db.commit()
    return True