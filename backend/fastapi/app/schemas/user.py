from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
