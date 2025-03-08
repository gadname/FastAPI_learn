from pydantic import BaseModel
from datetime import datetime


class BotBase(BaseModel):
    name: str = ""
    color: str = "C5E24A"


class BotCreate(BotBase):
    pass


class BotResponse(BotBase):
    id: int
    created_at: datetime
    updated_at: datetime
