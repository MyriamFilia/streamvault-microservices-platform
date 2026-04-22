from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Review
from app.schemas import ReviewCreate, ReviewUpdate, ReviewResponse
from app.auth import get_current_user_id

router = APIRouter(prefix="/reviews", tags=["Reviews"])

# ── Créer un avis ─────────────────────────────────────────────
@router.post("/", response_model=ReviewResponse, status_code=201)
def add_review(
    review: ReviewCreate, 
    user_id: int = Depends(get_current_user_id), 
    db: Session = Depends(get_db)
):
    existing_review = db.query(Review).filter(
        Review.user_id == user_id, 
        Review.series_id == review.series_id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=400, 
            detail="Vous avez déjà noté cette série. Utilisez la modification."
        )

    # TODO : Vérification gRPC du series-service ici

    new_review = Review(
        user_id=user_id, 
        series_id=review.series_id,
        rating=review.rating,
        comment=review.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

# ── Modifier un avis (NOUVEAU grâce à updated_at) ─────────────
@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    review = db.query(Review).filter(
        Review.id == review_id, 
        Review.user_id == user_id
    ).first()
    
    if not review:
        raise HTTPException(status_code=404, detail="Avis introuvable ou non autorisé")
    
    # Mise à jour des champs
    review.rating = review_update.rating
    review.comment = review_update.comment
    
    db.commit()
    db.refresh(review) # SQLAlchemy mettra à jour 'updated_at' automatiquement
    return review

# ── Récupérer les avis d'une série ────────────────────────────
@router.get("/series/{series_id}", response_model=list[ReviewResponse])
def get_reviews_for_series(
    series_id: int, 
    db: Session = Depends(get_db)
):
    return db.query(Review).filter(Review.series_id == series_id).all()

# ── Récupérer mes avis ─────────────────────────────────────────
@router.get("/me", response_model=list[ReviewResponse])
def get_my_reviews(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    reviews = db.query(Review).filter(
        Review.user_id == user_id
    ).all()

    return reviews


# ── Supprimer un avis ─────────────────────────────────────────
@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int, 
    user_id: int = Depends(get_current_user_id), 
    db: Session = Depends(get_db)
):
    review = db.query(Review).filter(
        Review.id == review_id, 
        Review.user_id == user_id
    ).first()
    
    if not review:
        raise HTTPException(status_code=404, detail="Avis introuvable")
    
    db.delete(review)
    db.commit()
    return

# ── Health check ──────────────────────────────────────────────
@router.get("/health")
def health():
    return {"status": "UP", "service": "review-service"}