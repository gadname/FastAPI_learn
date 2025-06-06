from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CatCreate(BaseModel):
    name: str
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None


class CatResponse(BaseModel):
    id: str
    name: str
    breed: Optional[str]
    age: Optional[int]
    weight: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class CatAllResponse(BaseModel):
    cats: List[CatResponse]


class UpdateCatRequest(BaseModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None


class UpdateCatResponse(BaseModel):
    id: str
    name: str
    breed: Optional[str]
    age: Optional[int]
    weight: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class DeleteCatResponse(BaseModel):
    message: str
    id: str