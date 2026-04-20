# Series Microservices Platform

Projet microservices sur les séries TV.

## Architecture

- series-service (FastAPI)
- frontend (HTML/CSS/JS + Nginx)
- Docker / docker-compose
- Kubernetes + Minikube
- Service Mesh avec Istio
- Istio Gateway + VirtualService

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

### Avec Kubernetes + Istio

```bash
minikube start

istioctl install --set profile=demo -y

kubectl label namespace default istio-injection=enabled

kubectl apply -f k8s/series-deployment.yaml
kubectl apply -f k8s/series-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml

kubectl apply -f k8s/istio-gateway.yaml
kubectl apply -f k8s/virtual-service.yaml

kubectl rollout restart deployment frontend-deployment
kubectl rollout restart deployment series-service-deployment

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

### Kubernetes + Istio

Frontend :  
http://series.local

Backend :  
http://series.local/api

Swagger :  
http://series.local/api/docs

## Configuration hosts

Ajouter dans le fichier hosts :

```text
127.0.0.1 series.local
```

Sous Windows :

```text
C:\Windows\System32\drivers\etc\hosts
```
