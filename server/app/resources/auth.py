from flask_restful import Resource, reqparse
from mongoengine import NotUniqueError
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    create_refresh_token,
    get_jwt_identity,
)
from app.models.user import User
import bcrypt
from flask_jwt_extended import get_jwt
from flask import jsonify
from app.models.revoked_token import RevokedToken

parserSignup = reqparse.RequestParser()
parserSignup.add_argument(
    "email", type=str, required=True, help="Email cannot be blank"
)
parserSignup.add_argument(
    "password", type=str, required=True, help="Password cannot be blank"
)
parserSignup.add_argument(
    "first_name", type=str, required=True, help="First name cannot be blank"
)
parserSignup.add_argument(
    "last_name", type=str, required=True, help="Last name cannot be blank"
)


class SignupResource(Resource):
    """
    Resource for user signup.

    Parameters
    ----------
    email : str
        Email of the user, must be provided.
    password : str
        Password of the user, must be provided.
    first_name : str
        First name of the user, must be provided.
    last_name : str
        Last name of the user, must be provided.

    Returns
    -------
    str
        Access token upon successful signup.

    Raises
    ------
    dict
        Error message and status code if user with the provided email already exists or if an unexpected error occurs during signup.
    """

    def post(self):
        """
        Handles HTTP POST request for user signup.

        Returns
        -------
        str
            Access token upon successful signup.
        """
        try:
            args = parserSignup.parse_args()

            if User.objects(email=args["email"]):
                return {"error": "Email already exists"}, 401

            password = args["password"]
            password = str.encode(password)
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(16))

            new_user = User(
                first_name=args["first_name"],
                last_name=args["last_name"],
                email=args["email"],
                hashed_password=hashed_password,
            )
            new_user.save()

            access_token = create_access_token(identity=new_user, fresh=True)
            refresh_token = create_refresh_token(identity=new_user)

            return {
                "user": {
                    "id": str(new_user.id),
                    "firstName": new_user.first_name,
                    "lastName": new_user.last_name,
                    "followers": new_user.followers,
                    "following": new_user.following,
                },
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500


parserLogin = reqparse.RequestParser()
parserLogin.add_argument("email", type=str, required=True, help="Email cannot be blank")
parserLogin.add_argument(
    "password", type=str, required=True, help="Password cannot be blank"
)


class LoginResource(Resource):
    """
    Resource for user login.

    Parameters
    ----------
    email : str
        Email of the user, must be provided.
    password : str
        Password of the user, must be provided.

    Returns
    -------
    str
        Access token upon successful login.

    Raises
    ------
    dict
        Error message and status code if provided email does not exist, if the password is incorrect, or if an unexpected error occurs during login.
    """

    def post(self):
        """
        Handles HTTP POST request for user login.

        Returns
        -------
        str
            Access token upon successful login.
        """
        try:
            args = parserLogin.parse_args()
            user = User.objects(email=args["email"]).first()

            if not user:
                return {"error": "Wrong email or password"}, 402

            password = args["password"]
            password = str.encode(password)

            if not bcrypt.checkpw(password, str.encode(user.hashed_password)):
                return {"error": "Wrong email or password"}, 401

            access_token = create_access_token(identity=user, fresh=True)
            refresh_token = create_refresh_token(identity=user)

            return {
                "user": {
                    "id": str(user.id),
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "followers": user.followers,
                    "following": user.following,
                },
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

        except Exception as e:
            print(e)
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500


class LogoutResource(Resource):
    """
    Resource for user logout.

    Returns
    -------
    str
        Message indicating successful token revocation.

    Raises
    ------
    dict
        Error message and status code if an unexpected error occurs during token revocation.
    """

    @jwt_required()
    def delete(self):
        """
        Handles HTTP DELETE request for user logout.

        Returns
        -------
        str
            Message indicating successful token revocation.
        """
        try:
            jti = get_jwt()["jti"]
            RevokedToken(jti=jti).save()
            return jsonify(msg="Access token revoked")

        except Exception as e:
            print(e)
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500


class RefreshResource(Resource):
    """
    Resource for refreshing access token.

    Returns
    -------
    str
        New access token.

    Raises
    ------
    dict
        Error message and status code if an unexpected error occurs during token refresh.
    """

    @jwt_required(refresh=True)
    def post(self):
        """
        Handles HTTP POST request for token refresh.

        Returns
        -------
        str
            New access token.
        """
        try:
            identity = get_jwt_identity()
            user = {"id": identity}
            access_token = create_access_token(identity=user, fresh=False)
            return jsonify(access_token=access_token)

        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500
