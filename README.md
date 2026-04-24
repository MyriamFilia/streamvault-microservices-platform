# Plateforme de Séries TV - Architecture Microservices

Ce projet est une plateforme de découverte et de gestion de séries TV. Il repose sur une architecture microservices robuste, scalable et conteneurisée, gérée par Kubernetes et sécurisée par Istio.

## Architecture Technique

### Les Microservices (FastAPI)

L'application est divisée en 4 services backend indépendants et un frontend :

- **Series Service** : Proxy vers l'API publique TVMaze pour la recherche de séries. Il agit également comme **Serveur gRPC** (port 50051) pour valider l'existence des séries pour les autres services.
- **User Service** : Gestion des utilisateurs, inscription, et génération de tokens d'authentification (JWT).
- **Favorites Service** : Gestion des favoris utilisateurs. Agit comme **Client gRPC** pour vérifier l'existence d'une série avant l'ajout.
- **Review Service** : Gestion des notes et commentaires. Agit également comme **Client gRPC**.
- **Frontend** : Interface utilisateur construite en **Vue.js 3** (Composition API), compilée avec **Vite** et servie via un Reverse Proxy **Nginx**.
  Communique avec les services backend via des appels REST proxifiés par Nginx.

### Communication & Réseau

- **Trafic Externe** : Requêtes HTTP/REST classiques transitant par une Gateway (Nginx en local, Istio VirtualService sur K8s).
- **Trafic Interne** : Communication ultra-rapide en **gRPC** (Protobuf) entre les services pour les validations métier.

### Base de Données

- **PostgreSQL** : Une seule instance de base de données, partitionnée logiquement via un script `init.sql` (ConfigMap) pour isoler les données :
  - `userdb`
  - `favoritesdb`
  - `reviewdb`

---

## Stack Technologique & Infrastructure

- **Backend** : Python 3.10+, FastAPI, Pydantic, SQLAlchemy.
- **Communication** : gRPC, Protocol Buffers.
- **Conteneurisation** : Docker, Docker Compose.
- **Orchestration** : Kubernetes (Minikube).
- **Service Mesh** : Istio (Gateway, VirtualService).

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


# 4. Mettre en place les rôles de sécurité (RBAC)
kubectl apply -f k8s/security/service-account.yaml
kubectl apply -f k8s/security/rbac/roles.yaml
kubectl apply -f k8s/security/rbac/role-bindings.yaml


# 5. Déployer les microservices
kubectl apply -f k8s/

# 6. Activer le chiffrement militaire (mTLS STRICT) et la protection réseau
kubectl apply -f k8s/security/mtls.yaml
kubectl apply -f k8s/security/postgres-mtls-exception.yaml

# 7. Déployer tous les services
kubectl apply -f k8s/

# 8. Ouvrir le tunnel Minikube
minikube tunnel
```

---

## URLs d'accès

### Local (Docker Compose)

| Service    | URL                   | Swagger                        |
| ---------- | --------------------- | ------------------------------ |
| Frontend   | http://localhost:5500 | —                              |
| Series API | http://localhost:8000 | http://localhost:8000/api/docs |
| Users      | http://localhost:8002 | http://localhost:8002/docs     |
| Favorites  | http://localhost:8003 | http://localhost:8003/docs     |
| Reviews    | http://localhost:8004 | http://localhost:8004/docs     |

### Kubernetes + Istio

| Service    | URL                           | Swagger                            |
| ---------- | ----------------------------- | ---------------------------------- |
| Frontend   | http://series.local           | —                                  |
| Series API | http://series.local/api       | http://series.local/api/docs       |
| Users      | http://series.local/users     | http://series.local/users/docs     |
| Favorites  | http://series.local/favorites | http://series.local/favorites/docs |
| Reviews    | http://series.local/reviews   | http://series.local/reviews/docs   |

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

## Frontend (Vue.js 3)

L'interface utilisateur a été conçue pour offrir une expérience fluide et réactive (SPA - Single Page Application). Elle interagit avec les différents microservices de manière transparente.

**Fonctionnalités clés :**

- **Architecture par composants :** Utilisation de Vue 3 (Composition API avec `<script setup>`).
- **Routage dynamique :** Navigation fluide et protection des routes privées (Redirection automatique si non authentifié) via `vue-router`.
- **Gestion des requêtes & Intercepteurs :** Utilisation d'`Axios` avec des intercepteurs globaux. Le token JWT est injecté automatiquement dans les en-têtes de chaque requête. En cas d'expiration du token (Erreur 401), l'utilisateur est déconnecté proprement.
- **UI/UX sur mesure :** Modales interactives, système de notifications (Toasts) et design 100% responsive en CSS pur.
- **Serveur Nginx optimisé :** Le frontend est compilé puis servi par Nginx, configuré spécifiquement pour éviter les collisions de routes (`try_files`) et empêcher les redirections absolues liées à Docker.

---

## Jeu de Démo (Database Seeding)

Puisque l'architecture repose sur des bases de données isolées par microservices, l'insertion manuelle en SQL est proscrite (notamment à cause du hachage des mots de passe et de la cohérence des IDs).

Un script Python (`seed.py`) a été développé pour simuler un comportement utilisateur réel en attaquant directement l'API Gateway.

**Ce que fait le script :**

1. Création de 5 profils utilisateurs réalistes (ex: _Alice_Cinephile_).
2. Authentification et récupération des tokens JWT.
3. Sélection aléatoire de vraies séries via leurs identifiants TVMaze (ex: _Breaking Bad, Stranger Things_).
4. Ajout de séries en favoris.
5. Publication d'avis (Notes de 1 à 5) avec des commentaires textuels adaptés à la note générée.

### Lancer la simulation

Assurez-vous que le cluster Kubernetes est fonctionnel et que le tunnel (`minikube tunnel`) est actif.

````bash
# 1. Installer la dépendance HTTP si nécessaire
pip install requests

# 2. Exécuter le script
python seed.py

---

## Sécurité

### RBAC Kubernetes

Le cluster a été sécurisé avec **RBAC (Role-Based Access Control)** afin de limiter les permissions accordées aux workloads Kubernetes selon le principe du **moindre privilège**.

#### Mesures mises en place

- Un **ServiceAccount dédié** a été créé pour chaque service déployé.
- Le service `series-service` utilise le `ServiceAccount` `series-service-sa`.
- Un **Role** nommé `serie-role` a été créé dans le namespace `default`.
- Un **RoleBinding** nommé `serie-service-binding` associe ce rôle au `ServiceAccount` `series-service-sa`.

#### Permissions accordées

Le rôle `serie-role` autorise uniquement un accès **en lecture** aux ressources Kubernetes suivantes :

- `pods`
- `services`
- `endpoints`

Les actions autorisées sont limitées à :

- `get`
- `list`
- `watch`

Cette configuration permet de montrer un contrôle d’accès fin dans le cluster sans attribuer de permissions excessives aux autres microservices. Les autres services conservent leur identité propre via leurs `ServiceAccount`, mais ne disposent pas de permissions supplémentaires sur l’API Kubernetes.

#### Vérification

Les permissions ont été vérifiées avec la commande suivante :

```bash
kubectl auth can-i list pods --as=system:serviceaccount:default:series-service-sa
````

Résultat attendu :

```bash
yes
```

Une action non autorisée peut aussi être testée :

```bash
kubectl auth can-i delete pods --as=system:serviceaccount:default:series-service-sa
```

Résultat attendu :

```bash
no
```

#### Intérêt de cette configuration

Cette mise en place permet :

- d’éviter l’utilisation du `ServiceAccount` par défaut pour tous les pods ;
- de mieux isoler les services entre eux ;
- de limiter la surface d’attaque en cas de compromission d’un composant ;
- de démontrer l’utilisation concrète de RBAC dans Kubernetes.

### mTLS Istio

Le projet utilise mTLS STRICT avec Istio afin de chiffrer automatiquement les communications internes entre microservices.

- Sécuriser les échanges entre :
- favorites-service ↔ series-service
- review-service ↔ series-service
- user-service ↔ autres services

et empêcher toute communication non authentifiée dans le cluster.
Une politique `PeerAuthentication` en mode **STRICT** a été appliquée sur le namespace `default`.
Tout le trafic inter-services au sein du mesh est désormais chiffré et authentifié mutuellement.

#### Vérification

```bash
kubectl get peerauthentication -n default
```

Résultat attendu :

```bash
default               STRICT       X
postgres-permissive   PERMISSIVE   X
```

---

## Sécurité & Authentification Applicative (JWT)

Le service utilisateur (`user-service`) intègre un système d'authentification robuste basé sur les standards de l'industrie pour garantir la protection absolue des données et des accès utilisateurs.

### Mécanismes de Protection

- **Hachage des mots de passe (Bcrypt) :** Les mots de passe ne sont **jamais** stockés en clair dans la base de données. L'algorithme `bcrypt` est utilisé pour le hachage irréversible lors de l'inscription et pour la vérification cryptographique à la connexion.
- **Gestion Sécurisée des Clés :** La clé de signature des tokens est isolée via la variable d'environnement `SECRET_KEY` (chargée dynamiquement avec `os.getenv()`). Aucun secret n'est exposé en dur dans le code source.
- **Expiration des Jetons :** Afin de limiter la surface d'attaque en cas de vol de session, les JWT possèdent une durée de vie stricte et limitée (`ACCESS_TOKEN_EXPIRE_MINUTES = 30`).
- **Révocation et Blacklist :** Lors de l'appel à la route de déconnexion, le token actif est placé sur une liste noire (Blacklist) bloquant instantanément toute tentative de réutilisation du token révoqué.

### Routes Protégées

Le mécanisme de sécurité `HTTPBearer` agit comme un gardien sur les points d'entrée de l'API. Un jeton d'accès valide est obligatoirement requis dans le header `Authorization: Bearer <token>`pour accéder aux routes protégées (`/users/me`, `/favorites/`, `/reviews/`).

### 🎯 Bonnes Pratiques Globales (DevSecOps)

Ce projet ne se contente pas de sécuriser les routes, il applique une stratégie de **Défense en Profondeur** à tous les niveaux :

- **Validation stricte** et nettoyage des données d'entrée grâce à **Pydantic**.
- **Séparation des responsabilités** entre les microservices.
- **Principe du Moindre Privilège** via les _ServiceAccounts_ Kubernetes (RBAC).
- **Isolation réseau & Chiffrement de bout en bout** via **Istio Service Mesh** (mTLS Strict).
- **Injection sécurisée** des identifiants (Bases de données) via les _Secrets_ Kubernetes.

---

## Stack technique

| Technologie             | Usage                                        |
| ----------------------- | -------------------------------------------- |
| FastAPI                 | Framework backend Python                     |
| PostgreSQL              | Base de données relationnelle                |
| Docker / Docker Compose | Conteneurisation locale                      |
| Kubernetes / Minikube   | Orchestration                                |
| Istio                   | Service Mesh + Gateway                       |
| gRPC                    | Communication inter-services                 |
| JWT                     | Authentification                             |
| TVMaze API              | Source des données séries                    |
| Nginx                   | Reverse proxy frontend                       |
| Vue.js 3 / Vite         | Framework Frontend (Single Page Application) |
| Axios                   | Client HTTP Frontend & Intercepteurs         |
