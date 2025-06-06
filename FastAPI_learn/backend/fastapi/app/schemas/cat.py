from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CatBase(BaseModel):
    name: str
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None

class CatCreate(CatBase):
    pass

class CatUpdate(CatBase):
    name: Optional[str] = None

class Cat(CatBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True