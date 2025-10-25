from fastapi.testclient import TestClient
import pytest

# The 'client' fixture is auto-magically provided by conftest.py
# We also assume the auth user is 'johndoe' with password 'secret'
# as defined in step (2.5) auth.py

def test_get_token(client: TestClient):
    """
    Test 1: Successfully obtain an authentication token.
    """
    response = client.post(
        "/token",
        data={"username": "johndoe", "password": "secret"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"

def test_create_campaign_no_auth(client: TestClient):
    """
    Test 2: Fail to create a campaign without a valid token.
    """
    response = client.post(
        "/campaigns/",
        json={"name": "Test Campaign", "budget": 1000.0, "target_audience": "Everyone"}
    )
    assert response.status_code == 401  # Unauthorized
    assert response.json() == {"detail": "Not authenticated"}

def test_create_and_get_campaigns(client: TestClient):
    """
    Test 3 & 4: Create a campaign successfully with auth,
    and then retrieve the list of campaigns.
    """
    # First, get a token
    token_response = client.post(
        "/token",
        data={"username": "johndoe", "password": "secret"}
    )
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test 3: Create a campaign
    campaign_data = {
        "name": "Winter Sale",
        "budget": 5000.50,
        "target_audience": "Shoppers aged 25-45"
    }
    create_response = client.post(
        "/campaigns/",
        json=campaign_data,
        headers=headers
    )
    assert create_response.status_code == 200  # Or 201 if you set it in the endpoint
    created_campaign = create_response.json()
    assert created_campaign["name"] == campaign_data["name"]
    assert created_campaign["budget"] == campaign_data["budget"]
    assert "id" in created_campaign
    assert "owner_username" in created_campaign
    assert created_campaign["owner_username"] == "johndoe" # From token

    # Test 4: Retrieve the list of campaigns
    get_response = client.get("/campaigns/", headers=headers)
    assert get_response.status_code == 200
    campaign_list = get_response.json()

    assert isinstance(campaign_list, list)
    assert len(campaign_list) > 0
    # Check if the campaign we just created is in the list
    found = any(c["id"] == created_campaign["id"] and c["name"] == "Winter Sale" for c in campaign_list)
    assert found, "The newly created campaign was not found in the list."
