# Plateforme de Séries TV - Architecture Microservices

Ce projet est une plateforme de découverte et de gestion de séries TV. Il repose sur une architecture microservices robuste, scalable et conteneurisée, gérée par Kubernetes et sécurisée par Istio.

##  Architecture Technique

###  Les Microservices (FastAPI)
L'application est divisée en 4 services backend indépendants et un frontend :
* **Series Service** : Proxy vers l'API publique TVMaze pour la recherche de séries. Il agit également comme **Serveur gRPC** (port 50051) pour valider l'existence des séries pour les autres services.
* **User Service** : Gestion des utilisateurs, inscription, et génération de tokens d'authentification (JWT).
* **Favorites Service** : Gestion des favoris utilisateurs. Agit comme **Client gRPC** pour vérifier l'existence d'une série avant l'ajout.
* **Review Service** : Gestion des notes et commentaires. Agit également comme **Client gRPC**.
* **Frontend** : Interface utilisateur (HTML/CSS/JS - *Bientôt en Vue.js*) servie via un Reverse Proxy Nginx.

###  Communication & Réseau
* **Trafic Externe** : Requêtes HTTP/REST classiques transitant par une Gateway (Nginx en local, Istio VirtualService sur K8s).
* **Trafic Interne** : Communication ultra-rapide en **gRPC** (Protobuf) entre les services pour les validations métier.

### Base de Données
* **PostgreSQL** : Une seule instance de base de données, partitionnée logiquement via un script `init.sql` (ConfigMap) pour isoler les données :
  * `userdb`
  * `favoritesdb`
  * `reviewdb`

---

## Stack Technologique & Infrastructure
* **Backend** : Python 3.10+, FastAPI, Pydantic, SQLAlchemy.
* **Communication** : gRPC, Protocol Buffers.
* **Conteneurisation** : Docker, Docker Compose.
* **Orchestration** : Kubernetes (Minikube).
* **Service Mesh** : Istio (Gateway, VirtualService).

---

## Registre Docker Hub

Les images du projet sont versionnées et disponibles publiquement. 

```bash
docker pull myrafilia/series-service:v4
docker pull myrafilia/user-service:v3
docker pull myrafilia/favorites-service:v2
docker pull myrafilia/review-service:v2
docker pull myrafilia/frontend-service:v3
```

---

## Lancer le projet

### En local avec Docker Compose

```bash
docker compose up --build
```

### Avec Kubernetes + Istio

> ⚠️ Istio doit être installé **avant** d'appliquer les manifests K8s.

```bash
# 1. Démarrer Minikube
minikube start

# 2. Installer Istio
istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled

# 3. Déployer PostgreSQL
kubectl apply -f k8s/postgres/postgres-secret.yaml
kubectl apply -f k8s/postgres/postgres-storage.yaml
kubectl apply -f k8s/postgres/configmap.yaml
kubectl apply -f k8s/postgres/postgres-deployment.yaml
kubectl apply -f k8s/postgres/postgres-service.yaml

# 4. Déployer tous les services
kubectl apply -f k8s/

# 5. Ouvrir le tunnel Minikube
minikube tunnel
```

---

##  URLs d'accès

### Local (Docker Compose)

| Service | URL | Swagger |
|---|---|---|
| Frontend | http://localhost:5500 | — |
| Series API | http://localhost:8000 | http://localhost:8000/api/docs |
| Users | http://localhost:8002 | http://localhost:8002/docs |
| Favorites | http://localhost:8003 | http://localhost:8003/docs |
| Reviews | http://localhost:8004 | http://localhost:8004/docs |

### Kubernetes + Istio

| Service | URL | Swagger |
|---|---|---|
| Frontend | http://series.local | — |
| Series API | http://series.local/api | http://series.local/api/docs |
| Users | http://series.local/users | http://series.local/users/docs |
| Favorites | http://series.local/favorites | http://series.local/favorites/docs |
| Reviews | http://series.local/reviews | http://series.local/reviews/docs |

---

## Configuration des hosts

Ajouter dans le fichier hosts :

```text
127.0.0.1 series.local
```

Sous Windows :

```text
C:\Windows\System32\drivers\etc\hosts
```

---

## Tests

##
---

## Sécurité (à venir)

- RBAC Kubernetes (ServiceAccount + Role + RoleBinding)
- mTLS Istio (chiffrement inter-services)

---

## Stack technique

| Technologie | Usage |
|---|---|
| FastAPI | Framework backend Python |
| PostgreSQL | Base de données relationnelle |
| Docker / Docker Compose | Conteneurisation locale |
| Kubernetes / Minikube | Orchestration |
| Istio | Service Mesh + Gateway |
| gRPC | Communication inter-services |
| JWT | Authentification |
| TVMaze API | Source des données séries |
| Nginx | Reverse proxy frontend |