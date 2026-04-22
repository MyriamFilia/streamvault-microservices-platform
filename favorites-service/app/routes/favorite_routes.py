# favorites_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Favorite
from app.schemas import FavoriteCreate, FavoriteResponse
from app.auth import get_current_user_id

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)

# ── Ajouter un favori ────────────────────────────────────────
@router.post("/", response_model=FavoriteResponse, status_code=201)
def add_favorite(
    favorite: FavoriteCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # 1. Vérifier si l'utilisateur a déjà ajouté cette série
    existing_favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.series_id == favorite.series_id
    ).first()

    if existing_favorite:
        raise HTTPException(
            status_code=400,
            detail="Cette série est déjà dans vos favoris"
        )

    # =========================================================
    # TODO : ÉTAPE SUIVANTE (gRPC)
    #
    # Avant de sauvegarder, on devra interroger le series-service
    # via gRPC pour vérifier que la série avec l'ID
    # favorite.series_id existe réellement.
    #
    # Exemple futur :
    #
    # grpc_client.check_series_exists(favorite.series_id)
    #
    # Si la série n'existe pas :
    # → lever une HTTPException(404)
    #
    # Cela évite d'ajouter un favori invalide.
    # =========================================================

    # 2. Sauvegarder en base de données
    new_favorite = Favorite(
        user_id=user_id,
        series_id=favorite.series_id
    )

    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)

    return new_favorite


# ── Récupérer mes favoris ────────────────────────────────────
@router.get("/", response_model=list[FavoriteResponse])
def get_my_favorites(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # L'utilisateur récupère uniquement ses propres favoris
    favorites = db.query(Favorite).filter(
        Favorite.user_id == user_id
    ).all()

    return favorites


# ── Supprimer un favori ──────────────────────────────────────
@router.delete("/{favorite_id}")
def delete_favorite(
    favorite_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    favorite = db.query(Favorite).filter(
        Favorite.id == favorite_id,
        Favorite.user_id == user_id
    ).first()

    if not favorite:
        raise HTTPException(
            status_code=404,
            detail="Favori introuvable"
        )

    db.delete(favorite)
    db.commit()

    return {
        "message": "Favori supprimé"
    }


# ── Health check ─────────────────────────────────────────────
@router.get("/health")
def health():
    return {
        "status": "UP"
    }