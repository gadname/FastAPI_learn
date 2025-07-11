from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CatCreate(BaseModel):
    """
    新しい猫を作成するためのデータスキーマ。
    """
    name: str = Field(..., description="猫の名前", example="タマ")
    breed: Optional[str] = Field(None, description="猫の品種", example="アメリカンショートヘア")
    age: Optional[int] = Field(None, description="猫の年齢（歳）", example=3, ge=0, le=30)
    weight: Optional[float] = Field(None, description="猫の体重（kg）", example=4.5, ge=0.1, le=20.0)


class CatResponse(BaseModel):
    """
    猫の情報を返すためのデータスキーマ。
    """
    id: str = Field(..., description="猫の一意識別子", example="cat_12345abcde")
    name: str = Field(..., description="猫の名前", example="タマ")
    breed: Optional[str] = Field(None, description="猫の品種", example="アメリカンショートヘア")
    age: Optional[int] = Field(None, description="猫の年齢（歳）", example=3)
    weight: Optional[float] = Field(None, description="猫の体重（kg）", example=4.5)
    created_at: datetime = Field(..., description="作成日時")
    updated_at: Optional[datetime] = Field(None, description="最終更新日時")
    
    class Config:
        from_attributes = True


class CatAllResponse(BaseModel):
    """
    全ての猫の情報を返すためのデータスキーマ。
    """
    cats: List[CatResponse] = Field(..., description="猫のリスト")


class UpdateCatRequest(BaseModel):
    """
    猫の情報を更新するためのデータスキーマ。
    """
    name: Optional[str] = Field(None, description="更新する猫の名前", example="タマ")
    breed: Optional[str] = Field(None, description="更新する猫の品種", example="アメリカンショートヘア")
    age: Optional[int] = Field(None, description="更新する猫の年齢（歳）", example=3, ge=0, le=30)
    weight: Optional[float] = Field(None, description="更新する猫の体重（kg）", example=4.5, ge=0.1, le=20.0)


class UpdateCatResponse(BaseModel):
    """
    猫の更新結果を返すためのデータスキーマ。
    """
    id: str = Field(..., description="猫の一意識別子", example="cat_12345abcde")
    name: str = Field(..., description="猫の名前", example="タマ")
    breed: Optional[str] = Field(None, description="猫の品種", example="アメリカンショートヘア")
    age: Optional[int] = Field(None, description="猫の年齢（歳）", example=3)
    weight: Optional[float] = Field(None, description="猫の体重（kg）", example=4.5)
    created_at: datetime = Field(..., description="作成日時")
    updated_at: Optional[datetime] = Field(None, description="最終更新日時")
    
    class Config:
        from_attributes = True


class DeleteCatResponse(BaseModel):
    """
    猫の削除結果を返すためのデータスキーマ。
    """
    message: str = Field(..., description="削除結果のメッセージ", example="猫を削除しました")
    id: str = Field(..., description="削除された猫の一意識別子", example="cat_12345abcde")