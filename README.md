# Opti-Campaign

## Description

Opti-Campaign est une mini-application démontrant une stack technique ("stack") Ad Tech moderne. Elle fournit une interface simple pour créer, voir et gérer des campagnes publicitaires, alimentée par une API backend haute performance et un frontend réactif.

## Stack Technique

* **Backend :** FastAPI
* **Frontend :** Vue.js 3 (avec l'API de Composition)
* **Base de données :** PostgreSQL (gérée via SQLAlchemy)
* **Validation des données :** Pydantic
* **Authentification :** JWT (JSON Web Tokens)
* **Styling :** Tailwind CSS
* **Conteneurisation :** Docker & Docker Compose

## Installation et Exécution

Ce projet est entièrement conteneurisé. **Docker** et **Docker Compose** sont requis pour le faire fonctionner.

1.  **Clonez le dépôt :**
```sh
git clone [https://github.com/votre-utilisateur/opti-campaign.git](https://github.com/votre-utilisateur/opti-campaign.git)
cd opti-campaign
```

2.  **Construisez les conteneurs (Build) :**
Cette commande construit les images Docker pour les services backend (FastAPI) et frontend (Vue.js).
```sh
make build
```

3.  **Exécutez l'application (Run) :**
Cette commande démarre tous les services en utilisant `docker-compose`, y compris la base de données, le backend et le frontend.
```sh
make run
```

Une fois démarrée, l'application sera accessible aux adresses suivantes :
* **Frontend (Vue.js) :** `http://localhost:8080`
* **Backend (FastAPI) :** `http://localhost:8000`

## Documentation de l'API

L'API backend fournit une documentation interactive générée automatiquement. Une fois l'application lancée, vous pouvez y accéder :

* **Swagger UI :** `http://localhost:8000/docs`
* **ReDoc :** `http://localhost:8000/redoc`

## Choix Techniques

* **FastAPI :** Choisi pour ses hautes performances, ses capacités asynchrones et sa validation automatique des données grâce à son intégration étroite avec **Pydantic**. C'est idéal pour une conception "API-first".
* **Vue.js 3 :** Sélectionné pour son **API de Composition** réactive, qui permet une logique frontend mieux organisée, réutilisable et évolutive (scalable).
* **SQLAlchemy :** Fournit un ORM (Object-Relational Mapper) robuste pour des interactions efficaces et sécurisées avec la base de données, en abstrayant le SQL brut.
* **Docker :** Assure un environnement de développement et de production cohérent et isolé, simplifiant la gestion des dépendances et le déploiement.

## Structure du projet

```
opti-campaign/
├── backend/
│ ├── app/
│ │ ├── (1.3) database.py # Config SQLAlchemy
│ │ ├── (1.4) models.py # Modèles SQLAlchemy
│ │ ├── (1.5) schemas.py # Schémas Pydantic (Data Contract)
│ │ ├── (2.1) crud.py # Fonctions CRUD (logique DB)
│ │ ├── (2.2) dependencies.py # Dépendance Auth JWT
│ │ ├── (2.3) routers/
│ │ │ ├── (2.4) campaigns.py # Endpoints pour /campaigns
│ │ │ └── (2.5) auth.py # Endpoint pour /token
│ │ └── (2.6) main.py # App FastAPI (importe les routers)
│ ├── (3.1) tests/
│ │ └── (3.2) test_campaigns.py
│ └── (4.1) Dockerfile
├── frontend/
│ ├── src/
│ │ ├── (5.1) api/
│ │ │ └── (5.2) index.js # Appels API centralisés
│ │ ├── (5.3) components/
│ │ │ └── (5.4) CampaignForm.vue
│ │ ├── (5.5) router/
│ │ │ └── (5.6) index.js # Config Vue Router
│ │ ├── (5.7) views/
│ │ │ ├── (5.8) CampaignListView.vue
│ │ │ └── (5.9) CampaignFormView.vue
│ │ └── (5.10) App.vue
│ ├── (4.2) Dockerfile
│ └── (6.1) package.json
├── (4.3) docker-compose.yml
├── (3.3) .github/workflows/ci.yml
├── (4.4) Makefile
└── (7.1) README.md
```
