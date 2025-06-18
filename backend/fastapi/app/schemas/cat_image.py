from pydantic import BaseModel, HttpUrl

class CatImageResponse(BaseModel):
    url: HttpUrl
