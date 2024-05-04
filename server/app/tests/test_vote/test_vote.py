import pytest
import json
from flask import Flask
from flask.testing import FlaskClient
from server.app.models.user import User
from server.app.models.post import Post
from server.main import app as main_app
from server.app.resources.vote import VoteResource
from flask_jwt_extended import create_access_token
from server.app.tests.helpers import create_user, create_mock_user


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


def test_record_vote(client: FlaskClient):
    # Create a sample post
    with client.application.app_context():
        # Mock an authenticated user
        current_user = create_user()
        token = create_access_token(identity=current_user, fresh=True)

        post = Post(title="Test Post", content="Test Content", author=current_user)
        post.save()

        # Make a POST request to record a vote
        response = client.post(
            f"/vote/{post.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        # Assert that the response status code is 201
        assert response.status_code == 201

        # Assert that the response message indicates successful vote recording
        assert json.loads(response.data.decode("utf-8")) == {
            "message": "Vote recorded successfully by the current user"
        }


def test_remove_vote(client: FlaskClient):
    # Create a sample post
    # Mock an authenticated user
    current_user = create_user()
    token = create_access_token(identity=current_user, fresh=True)
    post = Post(title="Test Post", content="Test Content", author=current_user)
    post.save()

    # Record a vote before removing it
    post.update(add_to_set__votes=current_user.id)
    post.reload()

    # Verify that the vote has been recorded successfully
    assert len(post.votes) == 1

    # Make a DELETE request to remove the vote
    response = client.delete(
        f"/vote/{post.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    post.reload()

    # Assert that the response status code is 204
    assert response.status_code == 204

    # Assert that the vote has been removed successfully
    assert len(post.votes) == 0
