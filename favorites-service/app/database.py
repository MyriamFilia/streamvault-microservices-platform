import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. On récupère les variables d'environnement (définies dans Docker/K8s)
DB_USER = os.getenv("POSTGRES_USER", "favoritedbuser")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "favoritedbpass")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost") # Nom du service K8s ou Docker
DB_NAME = os.getenv("POSTGRES_DB", "favoritesdb")        # CIBLE LA BONNE DB

# 2. Construction de l'URL de connexion
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

# 3. Création du moteur (Engine)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 4. Création de la fabrique de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Base pour les modèles
Base = declarative_base()

# 6. Dépendance pour FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()