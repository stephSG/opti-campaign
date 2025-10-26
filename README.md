# opti-campaign

## Structure du projet

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

