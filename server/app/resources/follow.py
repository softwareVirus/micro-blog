from flask_restful import Resource
from app.models.user import User
from flask_jwt_extended import current_user, jwt_required
from flask import abort


class FollowResource(Resource):
    """
    Resource for handling user follows.

    Methods
    -------
    post(user_id)
        Follow a user by the current user.

    delete(user_id)
        Unfollow a user by the current user.
    """

    @jwt_required()
    def post(self, user_id):
        """
        Follow a user by the current user.

        Parameters
        ----------
        user_id : str
            The ID of the user to be followed.

        Returns
        -------
        dict
            A JSON response indicating the success or failure of the follow operation.

        Raises
        ------
        Exception
            If an unexpected error occurs during the follow process.
        """
        try:
            # Check if the user exists
            user = User.objects.get(id=user_id)

            # Check if the current user is trying to follow themselves
            if str(user.id) == str(current_user.id):
                return {"message": "You cannot follow yourself"}, 400

            # Check if the current user is already following the target user
            if str(user.id) in current_user.following:
                return {"message": "You are already following this user"}, 400

            # Add the target user to the current user's following list
            current_user.update(add_to_set__following=user)
            user.update(add_to_set__followers=current_user)
            return {"message": "User followed successfully"}, 201

        except User.DoesNotExist:
            return {"message": "User not found"}, 404
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500

    @jwt_required()
    def delete(self, user_id):
        """
        Unfollow a user by the current user.

        Parameters
        ----------
        user_id : str
            The ID of the user to be unfollowed.

        Returns
        -------
        dict
            A JSON response indicating the success or failure of the unfollow operation.

        Raises
        ------
        Exception
            If an unexpected error occurs during the unfollow process.
        """
        try:
            # Check if the user exists
            user = User.objects.get(id=user_id)
            # Check if the current user is already following the target user
            if user not in current_user.following:
                return {"message": "You are not following this user"}, 400

            # Remove the target user from the current user's following list
            current_user.update(pull__following=user)
            user.update(pull__followers=current_user)
            return {"message": "User unfollowed successfully"}, 204

        except User.DoesNotExist:
            return {"message": "User not found"}, 404
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500
