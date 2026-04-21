# Series Microservices Platform
Projet de plateforme de découverte de séries TV basé sur une architecture microservices avec FastAPI, Docker, Kubernetes, gRPC et Istio.

## Architecture

### Microservices
- series-service → recherche de séries via API publique (TVMaze)
- user-service → authentification JWT + gestion utilisateurs
- frontend → interface HTML/CSS/JS + Nginx reverse proxy

### Infrastructure
- Docker + docker-compose
- Kubernetes + Minikube
- Istio Service Mesh
- Istio Gateway + VirtualService
- PostgreSQL unique avec plusieurs bases :
    - userdb
    - favoritesdb
    - review

### Kubernetes PostgreSQL
- Secret
- Storage (PVC)
- ConfigMap (init.sql)
- Deployment
- Service

## Docker Hub

Images disponibles sur Docker Hub :

### Series Service

```bash
docker pull myrafilia/series-service:latest
docker run -p 8000:8000 myrafilia/series-service:latest
```

### User Service

```bash
docker pull myrafilia/user-service:latest
docker run -p 8000:8000 myrafilia/user-service:latest
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

### Avec Kubernetes + Istio
⚠️ Istio doit être installé avant de lancer les fichiers k8s, sinon le Gateway et le VirtualService ne fonctionneront pas.

```bash
minikube start

istioctl install --set profile=demo -y

kubectl label namespace default istio-injection=enabled

kubectl apply -f k8s/nt

minikube tunnel
```

## URLs

### Local

Frontend:  
http://localhost/5500

API Tv_maz Backend:  
http://localhost:8000
http://localhost:8000/docs

Users : 
http://localhost:8002
http://localhost:8002/docs

---

### Kubernetes + Istio

Frontend :  
http://series.local

Series API :  
http://series.local/api
Swagger :  
http://series.local/api/docs

Users :  
http://series.local/users
Swagger :  
http://users.local/users/docs

## Configuration hosts

Ajouter dans le fichier hosts :

```text
127.0.0.1 series.local
```

Sous Windows :

```text
C:\Windows\System32\drivers\etc\hosts
```
