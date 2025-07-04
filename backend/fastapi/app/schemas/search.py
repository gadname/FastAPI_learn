from pydantic import BaseModel


class SearchResponseItem(BaseModel):
    title: str
    url: str


class SearchResponse(BaseModel):
    results: list[SearchResponseItem]
