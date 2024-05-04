from flask_restful import Resource
from flask import jsonify
from flask_jwt_extended import current_user, jwt_required
from app.models.user import User
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


class Profile(Resource):
    """
    Resource for retrieving user profile information.

    This resource requires a valid JWT token for access.

    Attributes
    ----------
    current_user : User
        The authenticated user object obtained from the JWT token.

    Methods
    -------
    get()
        Retrieves and returns the user's full name and email in a JSON response.

    Raises
    ------
    ExpiredSignatureError
        If the provided JWT token has expired.
    InvalidTokenError
        If the provided JWT token is invalid.

    Returns
    -------
    jsonify
        A JSON response containing the user's full name and email.
    """

    @jwt_required(fresh=True)
    def get(self, user_id):
        """
        Handles HTTP GET request for retrieving user profile information.

        Returns
        -------
        jsonify
            A JSON response containing the user's full name and email.
        """
        try:
            user = User.objects(id=user_id).get()
            return user.to_dict()

        except ExpiredSignatureError:
            return {"error": "JWT token has expired"}, 401

        except InvalidTokenError:
            return {"error": "Invalid JWT token"}, 401

        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500
