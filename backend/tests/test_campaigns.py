import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# client, test_db, and auth_headers fixtures are provided by conftest.py


def test_create_campaign_unauthenticated(client: TestClient):
    """
    Test creating a campaign without authentication.
    Should return 401 Unauthorized.
    """
    response = client.post("/campaigns/", json={
        "name": "Unauthorized Campaign",
        "start_date": "2025-01-01",
        "end_date": "2025-01-31",
        "budget": 1000.0,
    })
    assert response.status_code == 401
    assert "detail" in response.json()


def test_create_campaign_authenticated_success(client: TestClient, auth_headers: dict):
    """
    Test creating a campaign with valid authentication.
    Should return 201 Created with campaign data.
    """
    response = client.post("/campaigns/", headers=auth_headers, json={
        "name": "Test Campaign 1",
        "description": "A campaign for testing",
        "start_date": "2025-01-01",
        "end_date": "2025-01-31",
        "budget": 5000.50,
        "status": True
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Campaign 1"
    assert data["description"] == "A campaign for testing"
    assert data["budget"] == 5000.50
    assert data["status"] is True
    assert data["id"] is not None


def test_create_campaign_authenticated_error_invalid_data(client: TestClient, auth_headers: dict):
    """
    Test creating a campaign with invalid data (missing required fields).
    Should return 422 Unprocessable Entity.
    """
    response = client.post("/campaigns/", headers=auth_headers, json={
        "name": "Invalid Campaign",
        # Missing start_date, end_date, and budget
    })
    assert response.status_code == 422


def test_read_campaigns_unauthenticated(client: TestClient):
    """
    Test reading campaigns without authentication.
    Should return 401 Unauthorized.
    """
    response = client.get("/campaigns/")
    assert response.status_code == 401


def test_read_campaigns_authenticated_empty(client: TestClient, auth_headers: dict):
    """
    Test reading campaigns when no campaigns exist.
    Should return 200 with empty list.
    """
    response = client.get("/campaigns/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_read_campaigns_authenticated_with_data(client: TestClient, auth_headers: dict):
    """
    Test reading a list of campaigns with authentication after creating campaigns.
    Should return 200 with list of campaigns.
    """
    # Create first campaign
    client.post("/campaigns/", headers=auth_headers, json={
        "name": "List Test Campaign 1",
        "start_date": "2025-02-01",
        "end_date": "2025-02-28",
        "budget": 1234.0,
    })

    # Create second campaign
    client.post("/campaigns/", headers=auth_headers, json={
        "name": "List Test Campaign 2",
        "start_date": "2025-03-01",
        "end_date": "2025-03-31",
        "budget": 5678.0,
    })

    # Read all campaigns
    response = client.get("/campaigns/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "List Test Campaign 1"
    assert data[1]["name"] == "List Test Campaign 2"


def test_read_single_campaign(client: TestClient, auth_headers: dict):
    """
    Test reading a single campaign by ID.
    Should return 200 with campaign data.
    """
    # Create a campaign
    create_response = client.post("/campaigns/", headers=auth_headers, json={
        "name": "Single Campaign",
        "start_date": "2025-04-01",
        "end_date": "2025-04-30",
        "budget": 3000.0,
    })
    campaign_id = create_response.json()["id"]

    # Read the campaign
    response = client.get(f"/campaigns/{campaign_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == campaign_id
    assert data["name"] == "Single Campaign"
    assert data["budget"] == 3000.0


def test_update_campaign_success(client: TestClient, auth_headers: dict):
    """
    Test updating an existing campaign with valid data.
    Should return 200 with updated campaign data.
    """
    # Create campaign
    create_response = client.post("/campaigns/", headers=auth_headers, json={
        "name": "Campaign to Update",
        "start_date": "2025-03-01",
        "end_date": "2025-03-31",
        "budget": 100.0,
        "status": True
    })
    assert create_response.status_code == 201
    campaign_id = create_response.json()["id"]

    # Update campaign
    update_response = client.put(
        f"/campaigns/{campaign_id}",
        headers=auth_headers,
        json={
            "name": "Updated Campaign Name",
            "budget": 250.75,
            "status": False
        }
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Updated Campaign Name"
    assert data["budget"] == 250.75
    assert data["status"] is False
    # Ensure other fields were preserved
    assert data["start_date"] == "2025-03-01"
    assert data["end_date"] == "2025-03-31"


def test_update_campaign_unauthenticated(client: TestClient, auth_headers: dict):
    """
    Test updating a campaign without authentication.
    Should return 401 Unauthorized.
    """
    # Create campaign first (with auth)
    create_response = client.post("/campaigns/", headers=auth_headers, json={
        "name": "Campaign",
        "start_date": "2025-05-01",
        "end_date": "2025-05-31",
        "budget": 500.0,
    })
    campaign_id = create_response.json()["id"]

    # Try to update without auth
    response = client.put(f"/campaigns/{campaign_id}", json={
        "name": "Should Fail"
    })
    assert response.status_code == 401


def test_update_campaign_not_found(client: TestClient, auth_headers: dict):
    """
    Test updating a non-existent campaign.
    Should return 404 Not Found.
    """
    response = client.put(
        "/campaigns/99999",
        headers=auth_headers,
        json={"name": "Non-existent"}
    )
    assert response.status_code == 404


def test_delete_campaign_success(client: TestClient, auth_headers: dict):
    """
    Test deleting an existing campaign.
    Should return 204 No Content or 200.
    """
    # Create campaign
    create_response = client.post("/campaigns/", headers=auth_headers, json={
        "name": "Campaign to Delete",
        "start_date": "2025-06-01",
        "end_date": "2025-06-30",
        "budget": 750.0,
    })
    campaign_id = create_response.json()["id"]

    # Delete campaign
    delete_response = client.delete(f"/campaigns/{campaign_id}", headers=auth_headers)
    assert delete_response.status_code in [200, 204]

    # Verify it's deleted by trying to read it
    get_response = client.get(f"/campaigns/{campaign_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_delete_campaign_unauthenticated(client: TestClient, auth_headers: dict):
    """
    Test deleting a campaign without authentication.
    Should return 401 Unauthorized.
    """
    # Create campaign first (with auth)
    create_response = client.post("/campaigns/", headers=auth_headers, json={
        "name": "Campaign",
        "start_date": "2025-07-01",
        "end_date": "2025-07-31",
        "budget": 300.0,
    })
    campaign_id = create_response.json()["id"]

    # Try to delete without auth
    response = client.delete(f"/campaigns/{campaign_id}")
    assert response.status_code == 401


def test_delete_campaign_not_found(client: TestClient, auth_headers: dict):
    """
    Test deleting a non-existent campaign.
    Should return 404 Not Found.
    """
    response = client.delete("/campaigns/99999", headers=auth_headers)
    assert response.status_code == 404


def test_authentication_flow(client: TestClient, test_db: Session):
    """
    Test the complete authentication flow:
    1. Create a user
    2. Obtain a token
    3. Use the token to access protected endpoints
    """
    from app import crud, schemas

    # Create user
    user_data = schemas.UserCreate(username="authtest", password="authpass123")
    crud.create_user(db=test_db, user=user_data)

    # Obtain token
    token_response = client.post(
        "/token",
        data={"username": "authtest", "password": "authpass123"}
    )
    assert token_response.status_code == 200
    token_data = token_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # Use token to create a campaign
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    campaign_response = client.post(
        "/campaigns/",
        headers=headers,
        json={
            "name": "Auth Test Campaign",
            "start_date": "2025-08-01",
            "end_date": "2025-08-31",
            "budget": 2000.0,
        }
    )
    assert campaign_response.status_code == 201


def test_authentication_invalid_credentials(client: TestClient):
    """
    Test authentication with invalid credentials.
    Should return 401 Unauthorized.
    """
    response = client.post(
        "/token",
        data={"username": "wronguser", "password": "wrongpass"}
    )
    assert response.status_code == 401
