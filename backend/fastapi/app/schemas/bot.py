from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BotBase(BaseModel):
    """
    チャットボットの基本情報を定義するベースクラス。
    """
    name: str = Field(default="", description="ボットの名前", example="アシスタントボット")
    color: str = Field(default="C5E24A", description="ボットの色コード（HEX形式）", example="FF5733")


class BotCreate(BotBase):
    """
    新しいチャットボットを作成するためのデータスキーマ。
    """
    pass


class UpdateBotRequest(BaseModel):
    """
    チャットボットの情報を更新するためのデータスキーマ。
    """
    name: Optional[str] = Field(None, description="更新するボットの名前", example="新しいアシスタント")
    color: Optional[str] = Field(None, description="更新するボットの色コード（HEX形式）", example="33FF57")


class BotResponse(BotBase):
    """
    チャットボットの情報を返すためのデータスキーマ。
    """
    id: str = Field(..., description="ボットの一意識別子", example="bot_12345abcde")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="最終更新日時")

    class Config:
        from_attributes = True


class BotAllResponse(BaseModel):
    """
    全てのチャットボットの情報を返すためのデータスキーマ。
    """
    bots: list[BotResponse] = Field(..., description="チャットボットのリスト")


class UpdateBotResponse(BaseModel):
    """
    チャットボットの更新結果を返すためのデータスキーマ。
    """
    id: str = Field(..., description="ボットの一意識別子", example="bot_12345abcde")
    name: str = Field(..., description="ボットの名前", example="アシスタントボット")
    color: str = Field(..., description="ボットの色コード（HEX形式）", example="C5E24A")
    updated_at: datetime = Field(..., description="最終更新日時")

    class Config:
        from_attributes = True


class DeleteBotResponse(BaseModel):
    """
    チャットボットの削除結果を返すためのデータスキーマ。
    """
    id: str = Field(..., description="削除されたボットの一意識別子", example="bot_12345abcde")
