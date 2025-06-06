from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from cruds import cat as cat_crud
from schemas.cat import Cat, CatCreate, CatUpdate
from db.session import get_db

router = APIRouter()

@router.get("/cats/", response_model=List[Cat])
def read_cats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    全ての猫の情報を取得します。
    """
    cats = cat_crud.get_cats(db, skip=skip, limit=limit)
    return cats

@router.get("/cats/{cat_id}", response_model=Cat)
def read_cat(cat_id: int, db: Session = Depends(get_db)):
    """
    指定されたIDの猫の情報を取得します。
    """
    db_cat = cat_crud.get_cat(db, cat_id=cat_id)
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return db_cat

@router.post("/cats/", response_model=Cat, status_code=status.HTTP_201_CREATED)
def create_cat(cat: CatCreate, db: Session = Depends(get_db)):
    """
    新しい猫の情報を作成します。
    """
    return cat_crud.create_cat(db=db, cat=cat)

@router.put("/cats/{cat_id}", response_model=Cat)
def update_cat(cat_id: int, cat: CatUpdate, db: Session = Depends(get_db)):
    """
    指定されたIDの猫の情報を更新します。
    """
    db_cat = cat_crud.update_cat(db=db, cat_id=cat_id, cat=cat)
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return db_cat

@router.delete("/cats/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    """
    指定されたIDの猫の情報を削除します。
    """
    success = cat_crud.delete_cat(db=db, cat_id=cat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cat not found")
    return None