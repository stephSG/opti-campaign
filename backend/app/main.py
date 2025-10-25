# This is the main entry point for the FastAPI application.
# It initializes the app, database, middleware, and includes all routers.
# All code, comments, and docstrings are in English.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Use relative imports (.) for sibling modules and packages
from . import models, database
from .routers import auth, campaigns

# --- Database Initialization ---
# This command tells SQLAlchemy to create all tables based on the models
# (defined in models.py) if they don't already exist.
# In a production setup, this is typically handled by migration tools
# like Alembic, but this is fine for development.
models.Base.metadata.create_all(bind=database.engine)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Opti-Campaign API",
    description="API for managing marketing campaigns.",
    version="1.0.0",
    docs_url="/docs", # URL for Swagger UI
    redoc_url="/redoc" # URL for ReDoc
)

# --- CORS Middleware ---
# Configure Cross-Origin Resource Sharing (CORS)
# This allows the frontend (running on a different domain)
# to make requests to this backend API.

# WARNING: allow_origins=["*"] is insecure for production.
# For production, you should list your specific frontend domain(s).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, PUT, etc.)
    allow_headers=["*"], # Allows all headers
)

# --- Include Routers ---
# Mount the routers from the routers module
# The auth router handles the /token endpoint
app.include_router(auth.router)
# The campaigns router handles all /campaigns endpoints
app.include_router(campaigns.router)

# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    """
    A simple health check endpoint.
    """
    return {"message": "Welcome to the Opti-Campaign API!"}

