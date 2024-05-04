import pytest
import jwt
from datetime import timedelta, datetime
from flask import Flask, jsonify
from flask.testing import FlaskClient
from main import app as main_app
from app.models.user import User
from app.models.post import Post
from app.models.revoked_token import RevokedToken
from mongomock import MongoClient
import bcrypt
from unittest.mock import patch
from flask_jwt_extended import decode_token, current_user
from flask_jwt_extended import create_access_token, create_refresh_token
import os, json
from app.tests.helpers import create_user

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


def test_get_all_posts(client: FlaskClient):
    # Mock Post.objects() method to return a list of sample posts
    with client.application.app_context():
        with patch("app.resources.post.Post.objects") as mock_objects:
            user = create_user()
            token = create_access_token(identity=user, fresh=True)
            sample_posts = [
                Post(title="Post 1", content="Content 1", author=user),
                Post(title="Post 1", content="Content 2", author=user),
            ]
            mock_objects.return_value = sample_posts
            # Make a GET request to the /posts endpoint
            response = client.get(
                "/posts", headers={"Authorization": f"Bearer {token}"}
            )
            # Assert that the response status code is 200
            assert response.status_code == 200
            # Assert that the response data matches the sample posts
            assert json.loads(response.data.decode("utf-8")) == [
                post.to_dict() for post in sample_posts
            ]


def test_create_post(client: FlaskClient):
    # Mock the request parser to parse sample post data
    sample_post_data = {"title": "New Post", "content": "New Content"}
    with patch("app.resources.post.parserPost.parse_args") as mock_parse_args:
        mock_parse_args.return_value = sample_post_data
        # Mock the current_user attribute to represent an authenticated user
        User.objects().delete()
        user = create_user()
        token = create_access_token(identity=user, fresh=True)
        # Mock the Post.save() method to return a sample post
        with patch("app.resources.post.Post.save") as mock_save:
            mock_save.return_value = sample_post_data
            # Make a POST request to the /posts endpoint
            response = client.post(
                "/posts",
                json=sample_post_data,
                headers={"Authorization": f"Bearer {token}"},
            )
            # Assert that the response status code is 201
            assert response.status_code == 201
            # Assert that the response data matches the sample post
            created_post = json.loads(response.data.decode("utf-8"))
            assert {
                "title": created_post["title"],
                "content": created_post["content"],
            } == sample_post_data


def test_delete_post(client: FlaskClient):
    # Create a sample post to delete
    sample_post_data = {"title": "To Be Deleted", "content": "Delete Me"}
    User.objects().delete()
    user = create_user()
    token = create_access_token(identity=user, fresh=True)
    post = Post(
        title=sample_post_data["title"],
        content=sample_post_data["content"],
        author=user,
    )
    post.save()
    another_user = create_user()
    token_another_user = create_access_token(identity=another_user, fresh=True)
    # Attempt to delete a post created by another user
    response = client.delete(
        f"/posts/{post.id}", headers={"Authorization": f"Bearer {token_another_user}"}
    )
    # Assert that the response status code is 403
    assert response.status_code == 403
    # Assert that the response message indicates lack of permission
    assert json.loads(response.data.decode("utf-8")) == {
        "error": "You don't have permission to delete this post"
    }
    # Attempt to delete the post
    response = client.delete(
        f"/posts/{post.id}", headers={"Authorization": f"Bearer {token}"}
    )
    # Assert that the response status code is 200
    assert response.status_code == 200
    # Assert that the response message indicates successful deletion
    assert json.loads(response.data.decode("utf-8")) == {
        "message": "Post deleted successfully"
    }
    # Assert that the post is actually deleted from the database
    assert Post.objects(id=post.id).count() == 0
    # Attempt to delete a non-existent post
    response = client.delete(
        "/posts/nonexistent_id", headers={"Authorization": f"Bearer {token}"}
    )
    # Assert that the response status code is 404
    assert response.status_code == 403
    # Assert that the response message indicates the post was not found
    assert json.loads(response.data.decode("utf-8")) == {"error": "Post not found"}

    # Create a new user to test deletion of another user's post
