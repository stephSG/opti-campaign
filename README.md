# Opti-Campaign

## Description

Opti-Campaign is a mini-application demonstrating a modern Ad Tech technology stack. It provides a simple interface to create, view, and manage advertising campaigns, powered by a high-performance backend API and a reactive frontend.

## Tech Stack

* **Backend:** FastAPI
* **Frontend:** Vue.js 3 (with Composition API)
* **Database:** SQLite (managed via SQLAlchemy)
* **Data Validation:** Pydantic
* **Authentication:** JWT (JSON Web Tokens)
* **Styling:** Tailwind CSS
* **Containerization:** Docker & Docker Compose

## Installation and Running

This project is fully containerized. **Docker** and **Docker Compose** are required to run it.

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/opti-campaign.git
    cd opti-campaign
    ```

2.  **Build the containers:**
    This command builds the Docker images for both backend (FastAPI) and frontend (Vue.js) services.
    ```sh
    make build
    ```

3.  **Run the application:**
    This command starts all services using `docker-compose`, including the database, backend, and frontend.
    ```sh
    make run
    ```

## Access

Once started, the application will be accessible at the following addresses:

*   **Frontend (Vue.js):** `http://localhost:5173/`
*   **Backend API:** `http://localhost:8000`
*   **API Documentation (Swagger UI):** `http://localhost:8000/docs`
*   **API Documentation (ReDoc):** `http://localhost:8000/redoc`

## Technical Choices

* **FastAPI:** Chosen for its high performance, asynchronous capabilities, and automatic data validation through tight integration with **Pydantic**. It's ideal for an "API-first" design.
* **Vue.js 3:** Selected for its reactive **Composition API**, which enables better organized, reusable, and scalable frontend logic.
* **SQLAlchemy:** Provides a robust ORM (Object-Relational Mapper) for efficient and secure database interactions, abstracting raw SQL.
* **Docker:** Ensures a consistent and isolated development and production environment, simplifying dependency management and deployment.

## Project Structure

```
opti-campaign/
├── backend/
│   ├── app/
│   │   ├── (1.3) database.py
│   │   ├── (1.4) models.py
│   │   ├── (1.5) schemas.py       # (Le "Data Contract")
│   │   ├── (2.1) crud.py
│   │   ├── (2.2) dependencies.py
│   │   ├── (2.3) routers/
│   │   │   ├── (2.4) campaigns.py
│   │   │   └── (2.5) auth.py
│   │   └── (2.6) main.py
│   ├── (3.1) tests/
│   │   └── (3.2) test_campaigns.py
│   └── (4.1) Dockerfile
├── frontend/
│   ├── src/
│   │   ├── (5.1) api/
│   │   │   └── (5.2) index.js         # (Helper Axios/fetch, utilisé par le store)
│   │   ├── (5.3) stores/
│   │   │   └── (5.4) campaignStore.js # (PINIA STORE)
│   │   ├── (5.5) components/
│   │   │   └── (5.6) CampaignForm.vue
│   │   ├── (5.7) router/
│   │   │   └── (5.8) index.js
│   │   ├── (5.9) views/
│   │   │   ├── (5.10) CampaignListView.vue
│   │   │   └── (5.11) CampaignFormView.vue
│   │   └── (5.12) App.vue
│   ├── (4.2) Dockerfile
│   └── (6.1) package.json         # (Doit inclure 'pinia' et 'axios')
├── (4.3) docker-compose.yml
├── (3.3) .github/workflows/ci.yml
├── (4.4) Makefile
└── (7.1) README.md
```

## Development

### Backend Development

To run the backend locally without Docker:

```sh
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload
```

### Frontend Development

To run the frontend locally without Docker:

```sh
cd frontend
npm install
npm run dev
```

## Testing

### Backend Tests

```sh
cd backend
pytest
```

### Frontend Tests

```sh
cd frontend
npm run test
```

To run tests using Docker (recommended for CI/CD):

*   **Backend Tests:**
    ```sh
    make test-backend
    ```

*   **Frontend Tests:**
    ```sh
    make test-frontend
    ```

## Default Credentials

* **Username:** `admin`
* **Password:** `admin123`

## License

This project is for demonstration purposes only.
