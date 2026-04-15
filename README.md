# Series Microservices Platform

Projet microservices sur les séries TV.

## Architecture
- series-service FastAPI
- frontend (HTML/CSS/JS + Nginx)
-  docker-compose
- Ingress Gateway

## Docker Hub
Images disponibles sur Docker Hub :

### Backend
```bash
docker pull myrafilia/series-service:latest
docker run -p 8000:8000 myrafilia/series-service:latest
```

### Frontend
```bash
docker pull myrafilia/frontend-service:latest
docker run -p 80:80 myrafilia/frontend-service:latest
```

## Lancer le projet

### En local avec docker-compose
```bash
docker compose up --build
```

### Avec Kubernetes
```bash
minikube start
minikube addons enable ingress

kubectl apply -f k8s/series-deployment.yaml
kubectl apply -f k8s/series-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
kubectl apply -f k8s/ingress.yaml

minikube tunnel
```

## URLs

### Local
Frontend:  
http://localhost:5500

Backend:  
http://localhost:8000

Swagger:  
http://localhost:8000/docs

---

### Kubernetes
Frontend:  
http://series.local

Backend:  
http://series.local/api

Swagger:  
http://series.local/api/docs

## Configuration hosts
Ajouter dans le fichier hosts :

```text
127.0.0.1 series.local
```
