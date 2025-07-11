from pydantic import BaseModel, Field, HttpUrl


class CatImageResponse(BaseModel):
    """
    猫の画像情報を返すためのデータスキーマ。
    """
    url: HttpUrl = Field(..., description="猫の画像URL", example="https://example.com/cat-image.jpg")
