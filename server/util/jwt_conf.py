from app.models.revoked_token import RevokedToken
from app.models.user import User
from datetime import timedelta
from flask_jwt_extended import JWTManager
import os
from flask import Blueprint

class JWTConfig:
    # Secret key to sign JWT tokens (you should keep this secret and not hardcode it here)
    SECRET_KEY = 'your_secret_key'
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    # Token expiration time
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

jwt = JWTManager()


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
