import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base
from app.dependencies import get_db

# --- Test Database Configuration ---
# Use SQLite in-memory database for tests (isolated and fast)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def test_db():
    """
    Create a fresh database for each test function.
    Yields a database session and cleans up after the test.
    """
    # Create a new engine for each test to ensure complete isolation
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Use StaticPool for in-memory database
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after the test
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture(scope="function")
def client(test_db: Session):
    """
    Create a TestClient with overridden database dependency.
    Each test gets a fresh client with a clean database.
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(test_db: Session):
    """
    Create a test user in the database.
    Returns the created user object.
    """
    from app import crud, schemas
    user_data = schemas.UserCreate(username="testuser", password="testpassword")
    user = crud.create_user(db=test_db, user=user_data)
    return user


@pytest.fixture(scope="function")
def auth_headers(client: TestClient, test_user):
    """
    Authenticate the test user and return headers with the access token.
    This fixture can be used to make authenticated requests.
    """
    # Login to get token
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200, f"Auth failed: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
