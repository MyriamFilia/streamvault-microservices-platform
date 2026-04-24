from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True) # L'ID de l'utilisateur
    series_id = Column(Integer, nullable=False)           # L'ID de la série
    added_at = Column(DateTime(timezone=True), server_default=func.now())