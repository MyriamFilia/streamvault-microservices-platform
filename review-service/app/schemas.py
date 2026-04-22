from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ReviewCreate(BaseModel):
    series_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: str

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    series_id: int
    rating: int
    comment: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}