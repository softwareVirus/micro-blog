import pytest
from flask import Flask
from flask.testing import FlaskClient
from main import app as main_app
from unittest.mock import patch
from flask_jwt_extended import decode_token
from flask_jwt_extended import create_access_token, create_refresh_token
from app.tests.helpers import create_user, create_mock_user

# Mock the request data
signup_data = {
    "email": "test123333122323213121312asasdasdas34@example.com",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User",
}

returnValue = None

@pytest.fixture(scope="module")
def app() -> Flask:
    """Create a Flask app instance for testing."""
    app = main_app
    yield app

@pytest.fixture(scope="module")
def client(app: Flask) -> FlaskClient:
    """Create a test client for the Flask app."""
    with app.test_client() as client:
        yield client

def test_signup(client: FlaskClient):
    """Test user signup."""
    response = client.post("/signup", json=signup_data)
    assert response.status_code == 200

def test_login(client: FlaskClient):
    """Test user login."""
    login_data = {"email": signup_data["email"], "password": "password123"}
    # Mock the expected user data
    with patch("app.models.user.User.objects.get") as query:
        user = create_mock_user()
        query.return_value = user
        response = client.post("/login", json=login_data)
        assert response.status_code == 200
        assert "access_token" in response.json

def test_logout(client: FlaskClient):
    """Test user logout."""
    response = client.delete("/logout", headers={"Authorization": f"Bearer jwt_token"})
    assert response.status_code == 500

    user = create_user()
    token = create_access_token(identity=user)
    # Send a DELETE request to logout endpoint
    response = client.delete("/logout", headers={"Authorization": f"Bearer {token}"})

    # Check response status code
    assert response.status_code == 200

    response = client.delete("/logout", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 500

def test_refresh(client: FlaskClient):
    """Test token refresh."""
    # Create a test user
    user = create_user()
    # Mock a refresh token
    token = create_refresh_token(user)

    response = client.post(
        "/refresh_token", headers={"Authorization": f"Bearer {token}"}
    )

    # Check response status code
    assert response.status_code == 200

    # Check if a new access token is returned
    assert "access_token" in response.json
