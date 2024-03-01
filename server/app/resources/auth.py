from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    create_refresh_token,
    get_jwt_identity,
)
from models.user import User
import bcrypt
from flask_jwt_extended import get_jwt
from flask import jsonify
from models.revoked_token import RevokedToken

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
            salt = bcrypt.gensalt(16)
            hashed_password = bcrypt.hashpw(password, salt=salt)

            new_user = User(
                first_name=args["first_name"],
                last_name=args["last_name"],
                email=args["email"],
                salt=salt,
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

            if not User.objects(email=args["email"]):
                return {"error": "Wrong email or password"}, 401

            password = args["password"]
            password = str.encode(password)
            user = User.objects.get(email=args["email"])

            if not bcrypt.checkpw(password, str.encode(user.hashed_password)):
                return {"error": "Wrong email or password"}, 401

            access_token = create_access_token(identity=user, fresh=True)
            refresh_token = create_refresh_token(identity=user)

            return {
                "user": {
                    "id": str(user.id),
                    "firstName": user.first_name,
                    "lastName": user.last_name,
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


class LogoutResource(Resource):
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

    @jwt_required()
    def delete(self):
        """
        Handles HTTP POST request for user login.

        Returns
        -------
        str
            Access token upon successful login.
        """
        try:
            jti = get_jwt()["jti"]
            RevokedToken.objects(jti=jti).delete()
            return jsonify(msg="Access token revoked")

        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500


class RefreshResource(Resource):
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

    @jwt_required(refresh=True)
    def post():
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        return jsonify(access_token=access_token)
