from flask_restful import Resource, reqparse
from server.app.models.post import Post
from mongoengine.errors import ValidationError, DoesNotExist
from flask_jwt_extended import current_user, jwt_required
from server.app.models.tag import Tag
from server.app.models.user import User
import ast
from flask import request


parserTag = reqparse.RequestParser()
parserTag.add_argument(
    "tag", type=str, location="json", required=True, help="Tag cannot be blank"
)


class TagResource(Resource):
    """
    A resource for managing tags.
    """

    @jwt_required(fresh=True)
    def get(self, user_id=None):
        """
        Retrieve all tags or tags associated with a specific user.

        Parameters
        ----------
        user_id : str, optional
            The ID of the user whose tags are to be retrieved. Default is None.

        Returns
        -------
        list of dict
            List of dictionaries representing tags.

        Raises
        ------
        Exception
            If an unexpected error occurs while retrieving tags.
        """

        try:
            if user_id is None:
                # If no user ID provided, retrieve all tags
                tags = Tag.objects()
                return [tag.to_dict() for tag in tags]

            user = User.objects(id=user_id).get()
            tags = user.tags
            return [tag.to_dict() for tag in tags], 200
        except Exception as e:
                return {"error": f"An unexpected error occurred: {str(e)}"}, 400

    @jwt_required(fresh=True)
    def post(self):
        """
        Create a new tag.

        Returns
        -------
        dict
            Dictionary representing the newly created tag.
        int
            HTTP status code indicating the success of the operation.

        Raises
        ------
        Exception
            If an unexpected error occurs while creating a tag.
        """
        try:
            # Parse request arguments
            args = parserTag.parse_args()

            # Create a new tag instance
            new_tag = Tag(
                tag=args["tag"],
            )

            # Save the new tag to the database
            new_tag.save()

            # Convert the new tag to a dictionary
            tag_dict = new_tag.to_dict()

            # Return the newly created tag and HTTP status code
            return tag_dict, 201
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 400
