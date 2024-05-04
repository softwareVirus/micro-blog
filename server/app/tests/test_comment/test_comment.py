import json
import pytest
from server.app.models.user import User
from server.main import app as main_app
from server.app.models.post import Post
from server.app.models.comment import Comment
from server.app.resources.comment import CommentResource
from server.app.tests.helpers import create_user, create_mock_user
from flask_jwt_extended import create_access_token
from flask import Flask
from flask.testing import FlaskClient


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


def test_add_comment(client: FlaskClient):
    # Create a sample post to add a comment to
    with client.application.app_context():

        # Mock an authenticated user
        current_user = create_user()
        token = create_access_token(identity=current_user, fresh=True)

        post = Post.objects.create(
            title="Test Post", content="Test Content", author=current_user
        )

        # Prepare the request data
        comment_data = {"content": "Test Comment"}

        # Make a POST request to add a comment to the post
        response = client.post(
            f"/posts/{post.id}/comments",
            json=comment_data,
            headers={"Authorization": f"Bearer {token}"},
        )

        # Assert that the response status code is 201
        assert response.status_code == 201

        # Assert that the response data matches the created comment
        created_comment = json.loads(response.data.decode("utf-8"))
        assert created_comment["content"] == comment_data["content"]
        assert created_comment["author"]["email"] == current_user.email


def test_get_post_comments(client):
    # Create a sample post with comments
    post = Post(title="Test Post", content="Test Content")
    post.save()
    current_user = create_user()
    token = create_access_token(identity=current_user, fresh=True)

    # Create sample comments
    comment1 = Comment(content="Comment 1", author=current_user)
    comment1.save()
    post.comments.append(comment1)
    comment2 = Comment(content="Comment 2", author=current_user)
    comment2.save()
    post.comments.append(comment2)
    post.save()

    # Make a GET request to retrieve comments for the post
    response = client.get(
        f"/posts/{post.id}/comments",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response data matches the sample comments
    retrieved_comments = json.loads(response.data.decode("utf-8"))
    assert len(retrieved_comments) == 2
    assert retrieved_comments[0]["content"] == comment1.content
    assert retrieved_comments[1]["content"] == comment2.content
    comment2.total_number_of_child_comments = (
        comment2.total_number_of_child_comments + 1
    )
    comment3 = Comment(
        content="Comment 3", author=current_user, parent_comment=comment2
    )
    comment3.save()
    comment2.save()

    response = client.get(
        f"/posts/{post.id}/comments/{comment2.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response data matches the sample comments
    retrieved_comments = json.loads(response.data.decode("utf-8"))
    assert len(retrieved_comments) == 1
    assert retrieved_comments[0]["content"] == comment3.content


def test_delete_comment(client):
    # Mock an authenticated user
    current_user = create_user()
    token = create_access_token(identity=current_user, fresh=True)

    # Create a sample post with a comment
    post = Post(title="Test Post", content="Test Content")
    post.save()

    comment = Comment(content="Test Comment", author=current_user)
    comment.save()
    post.comments.append(comment)
    post.save()

    # Make a DELETE request to delete the comment
    response = client.delete(
        f"/posts/{post.id}/comments/{comment.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response message indicates successful deletion
    assert json.loads(response.data.decode("utf-8")) == {
        "message": "Comment deleted successfully"
    }

    # Assert that the comment is actually deleted from the database
    assert Comment.objects(id=comment.id).count() == 0
