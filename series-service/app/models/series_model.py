from pydantic import BaseModel
from typing import Optional


class SeriesResponse(BaseModel):
    id: int
    name: str
    language: Optional[str] = None
    genres: list[str] = []
    summary: Optional[str] = None
    premiered: Optional[str] = None