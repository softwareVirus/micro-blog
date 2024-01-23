from flask import request
from flask_restful import Resource
from models.comment import Comment
from flask_jwt_extended import jwt_required


class ChildCommentResource(Resource):
    @jwt_required()
    def get(self, parent_comment_id):
        """
        Retrieve child comments based on the parent comment ID with pagination.

        Parameters
        ----------
        parent_comment_id : str
            The ID of the parent comment.

        Returns
        -------
        tuple
            A tuple containing a list of paginated child comments and HTTP status code (200).

        Raises
        ------
        Comment.DoesNotExist
            If the specified parent comment is not found.
        Exception
            If an unexpected error occurs.
        """
        try:
            # Retrieve child comments based on the parent comment ID
            child_comments = list(Comment.objects(parent_comment=parent_comment_id))
            child_comments = sorted(
                child_comments, key=lambda x: x.created_at, reverse=True
            )

            # Pagination parameters
            page = int(request.args.get("page", 1))
            per_page = int(request.args.get("per_page", 10))

            # Calculate start and end indices for pagination
            start_index = (page - 1) * per_page
            end_index = start_index + per_page

            # Apply pagination
            paginated_child_comments = [
                comment.to_dict() for comment in child_comments[start_index:end_index]
            ]

            return paginated_child_comments, 200

        except Comment.DoesNotExist:
            return {"error": "Comment not found"}, 404
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500
