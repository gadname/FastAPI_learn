from pydantic import BaseModel
from datetime import datetime


class BotBase(BaseModel):
    name: str = ""
    color: str = "C5E24A"


class BotCreate(BotBase):
    pass


# modelとの接続
class BotResponse(BotBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BotAllResponse(BaseModel):
    bots: list[BotResponse]
