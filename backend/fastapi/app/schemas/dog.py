from typing import Optional, List
from pydantic import BaseModel

class DogBase(BaseModel):
    name: str
    breed: Optional[str] = None
    age: Optional[int] = None

class DogCreate(DogBase):
    pass

class DogUpdate(BaseModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None

class DogResponse(DogBase):
    id: str

    class Config:
        orm_mode = True

class DogAllResponse(BaseModel):
    dogs: List[DogResponse]
    count: int
