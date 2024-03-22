from flask import Flask, jsonify
from flask_restful import Api
import os
from datetime import timedelta
from mongoengine import connect
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from app.models.user import User
import mongomock
from app.resources.auth import (
    LoginResource,
    SignupResource,
    LogoutResource,
    RefreshResource,
)
from app.resources.tag import TagResource
from app.resources.comment import CommentResource
from app.resources.post import PostResource
from app.resources.protected import Profile
from app.resources.vote import VoteResource
from app.resources.follow import FollowResource
from app.models.revoked_token import RevokedToken
from flask_cors import CORS
from app.util.util import ACCESS_EXPIRES
import json

load_dotenv()  # Load environment variables from .env.


# Connect to MongoDB using the provided connection string

errors = {
    "ExpiredSignatureError": {
        "message": "Unauthorized",
        "status": 401,
    },
}
app = Flask(__name__)
CORS(app)
api = Api(app, errors=errors)
# Set the JWT secret key, loaded from the environment variable for security
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret_key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    try:
        jti = jwt_payload["jti"]
        token_in_db = RevokedToken.objects(jti=jti).get()
        return token_in_db is not None
    except RevokedToken.DoesNotExist:
        return None


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
    return str(user["id"])


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
    "/posts/<string:post_id>/comments/<string:comment_id>",
)
api.add_resource(VoteResource, "/vote/<string:post_id>")
api.add_resource(FollowResource, "/follow/<string:user_id>")
api.add_resource(
    PostResource,
    "/posts",
    "/posts/<string:tags>",
    "/post/<string:post_id>",
    "/feed_posts",
    "/user_posts/<string:user_id>",
    "/user_posts/<string:user_id>/<string:tags>",
)
api.add_resource(SignupResource, "/signup")
api.add_resource(LoginResource, "/login")
api.add_resource(Profile, "/profile/<string:user_id>")
api.add_resource(LogoutResource, "/logout")
api.add_resource(RefreshResource, "/refresh_token")
api.add_resource(TagResource, "/tags", "/tags/<string:user_id>")


def create_app(mode="dev"):
    # with open(f"./config.json", "r") as f:
    #    config = json.load(f)
    print(mode)
    if mode == "dev":
        connect(
            host="mongodb+srv://hello:12053085408a@cluster0.pn5ujkz.mongodb.net/?retryWrites=true&w=majority"
        )  # host=config["dev"]["MONGODB_URI"])
    if mode == "test":
        connect(
            "mongoenginetest",
            host="mongodb://localhost",
            mongo_client_class=mongomock.MongoClient,
            uuidRepresentation="standard",
        )
    return app
