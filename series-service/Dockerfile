# 1. On part d'une image Python simple et officielle
FROM python:3.14-slim

# 2. On dit à Docker de travailler dans le dossier /app
WORKDIR /app

# 3. On copie le fichier des dépendances
COPY requirements.txt .

# 4. On installe les bibliothèques (FastAPI, Uvicorn, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# 5. On copie tout le reste du code (votre main.py)
COPY . .

# 6. On lance l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]