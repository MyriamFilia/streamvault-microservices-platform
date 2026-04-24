from pydantic import BaseModel
from datetime import datetime

class FavoriteCreate(BaseModel):
    series_id: int

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    series_id: int
    added_at: datetime

    model_config = {"from_attributes": True}

from pydantic import BaseModel
from datetime import datetime
