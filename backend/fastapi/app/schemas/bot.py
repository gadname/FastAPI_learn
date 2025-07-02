from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BotBase(BaseModel):
    name: str = ""
    color: str = "C5E24A"


class BotCreate(BotBase):
    pass


class UpdateBotRequest(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None


class BotResponse(BotBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BotAllResponse(BaseModel):
    bots: list[BotResponse]


class UpdateBotResponse(BaseModel):
    id: str
    name: str
    color: str
    updated_at: datetime

    class Config:
        from_attributes = True


class DeleteBotResponse(BaseModel):
    id: str
