from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse, UserUpdate, TokenResponse
from app.auth import hash_password, verify_password, create_access_token, decode_access_token

router = APIRouter(prefix="/users", tags=["Users"])
security = HTTPBearer()


# ── Inscription ──────────────────────────────────────────────
@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username déjà utilisé")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ── Connexion ─────────────────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Compte désactivé")

    token = create_access_token({
        "sub": str(user.id),
        "username": user.username
    })
    return {"access_token": token}


# ── Profil connecté ───────────────────────────────────────────
@router.get("/me", response_model=UserResponse)
def get_me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user


# ── Mise à jour profil ────────────────────────────────────────
@router.put("/me", response_model=UserResponse)
def update_me(
    updates: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    if updates.email:
        user.email = updates.email
    if updates.password:
        user.hashed_password = hash_password(updates.password)

    db.commit()
    db.refresh(user)
    return user


# ── Health check ──────────────────────────────────────────────
@router.get("/health")
def health():
    return {"status": "UP"}