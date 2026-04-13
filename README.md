# Series Microservices Platform

Projet microservices sur les séries TV.

## Architecture
- series-service (FastAPI)
- frontend (HTML/CSS/JS + Nginx)
- docker-compose

## Docker Hub
Image disponible sur Docker Hub :

```bash
docker pull myrafilia/series-service:latest
docker run -p 8000:8000 myrafilia/series-service:latest
```

## Lancer le projet
```bash
docker compose up --build
```

## URLs
Frontend:
http://localhost:5500

Backend:
http://localhost:8000

Swagger:
http://localhost:8000/docs
