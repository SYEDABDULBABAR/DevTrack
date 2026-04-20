import pytest
from fastapi.testclient import TestClient
from app.main import app  # Main FastAPI entry point

client = TestClient(app)

# 1. Test: User Registration
def test_register_user():
    response = client.post("/auth/register", json={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpassword123"
    })
    assert response.status_code == 201
    assert response.json()["status"] == "success"

# 2. Test: User Login (Token Generation)
def test_login_user():
    response = client.post("/auth/login", data={
        "username": "testuser@example.com",
        "password": "testpassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

# 3. Test: Unauthorized Access (Security Check)
def test_unauthorized_project_access():
    # Attempting to create a project without a valid bearer token
    response = client.post("/projects/", json={
        "title": "Hack Project",
        "description": "I don't have a token"
    })
    assert response.status_code == 401  # Should return Unauthorized

# 4. Test: Create Project (With Token)
def test_create_project():
    # First, authenticate to retrieve the access token
    login_res = client.post("/auth/login", data={
        "username": "testuser@example.com",
        "password": "testpassword123"
    })
    token = login_res.json()["access_token"]
    
    # Create a project using the retrieved token in headers
    response = client.post(
        "/projects/", 
        json={"title": "DevTrack Test Project", "description": "Testing project creation"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "DevTrack Test Project"

# 5. Test: Get My Profile (/users/me)
def test_get_current_user():
    # Authenticate to get the token
    login_res = client.post("/auth/login", data={
        "username": "testuser@example.com",
        "password": "testpassword123"
    })
    token = login_res.json()["access_token"]
    
    # Verify the profile endpoint returns the correct user data
    response = client.get(
        "/users/me", 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"