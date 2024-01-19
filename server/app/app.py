from flask import Flask
from flask_restful import Api
import os
from datetime import timedelta
from mongoengine import connect
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from models.user import User
from resources.auth import LoginResource, SignupResource
from resources.comment import CommentResource
from resources.post import PostResource
from resources.child_comment import ChildCommentResource
from resources.protected import Profile
from resources.vote import VoteResource
from flask_cors import CORS

load_dotenv()  # Load environment variables from .env.

# Connect to MongoDB using the provided connection string
connect(host=os.getenv("MONGODB_CONNECTION_STRING"))

app = Flask(__name__)
CORS(app)
api = Api(app)

# Set the JWT secret key, loaded from the environment variable for security
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret_key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)


@jwt.user_identity_loader
def user_identity_loader(user):
    """
    Callback function to get the identity of the current user.

    Parameters
    ----------
    user : User
        The current user.

    Returns
    -------
    str
        The user's identity (user ID).
    """
    return str(user.id)


@jwt.user_lookup_loader
def user_lookup_loader(_jwt_header, jwt_data):
    """
    Callback function to look up a user by identity in JWT data.

    Parameters
    ----------
    _jwt_header : dict
        The JWT header (not used in this function).
    jwt_data : dict
        The JWT data containing the user's identity.

    Returns
    -------
    User
        The user associated with the provided identity.
    """
    identity = jwt_data["sub"]
    return User.objects.get(id=identity)


# Define API routes and associate them with the respective resources
api.add_resource(
    CommentResource,
    "/posts/<string:post_id>/comments",
    "/posts/<string:post_id>/comments/<string:parent_comment_id>",
)
api.add_resource(VoteResource, "/vote/<string:post_id>")
api.add_resource(PostResource, "/posts", "/posts/<string:post_id>")
api.add_resource(
    ChildCommentResource, "/comments/<string:parent_comment_id>/child"
)
api.add_resource(SignupResource, "/signup")
api.add_resource(LoginResource, "/login")
api.add_resource(Profile, "/profile")

if __name__ == "__main__":
    # Run the Flask application in debug mode during development
    app.run(debug=True)
