FROM python:3.13-slim

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copie et installation des dépendances d'abord (cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Port exposé
EXPOSE 8000

# Lancement du service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]