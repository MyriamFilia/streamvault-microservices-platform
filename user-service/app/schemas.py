from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Schemas pour les utilisateurs
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Le schéma de connexion peut être différent du schéma de création, car il n'a pas besoin de l'email
class UserLogin(BaseModel):
    username: str
    password: str

# Le schéma de mise à jour permet de rendre les champs optionnels
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

# Le schéma de réponse inclut les champs que nous voulons exposer à l'utilisateur, sans le mot de passe
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

# Schéma pour la réponse de token JWT
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"