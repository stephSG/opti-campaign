import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import the main FastAPI app and database settings from our application
# We assume the 'app' directory is in the python path
# You might need to adjust imports based on your project structure
# (e.g., from app.main import app, from app.database import Base, get_db)
import sys
import os

# Add the backend directory to the Python path to find the 'app' module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.database import Base, get_db

# 1. Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# 2. Create a test database engine and session
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Use StaticPool for SQLite in-memory
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 3. Override the 'get_db' dependency
def override_get_db():
    """
    A dependency override to use the test database session.
    """
    database = None
    try:
        database = TestingSessionLocal()
        yield database
    finally:
        if database:
            database.close()

# Apply the override to the FastAPI app
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    """
    Pytest fixture to provide a TestClient.
    This fixture runs once per test module.
    It creates the database tables before tests and drops them after.
    """
    # Create all tables in the test database
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as c:
        yield c

    # Drop all tables after tests are done
    Base.metadata.drop_all(bind=engine)
