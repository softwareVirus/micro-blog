from flask_restful import Resource
from models.post import Post
from flask_jwt_extended import current_user, jwt_required
from flask import abort

class VoteResource(Resource):
    """
    Resource for handling post votes.

    Methods
    -------
    post(post_id)
        Record a vote for the current user on a post.

    delete(post_id)
        Remove the vote of the current user from a post.
    """

    @jwt_required(fresh=True)
    def post(self, post_id):
        """
        Record a vote for the current user on a post.

        Parameters
        ----------
        post_id : str
            The ID of the post.

        Returns
        -------
        dict
            A JSON response indicating the success or failure of the operation.

        Raises
        ------
        Exception
            If an unexpected error occurs during the vote recording process.
        """
        try:
            post = Post.objects.get_or_404(id=post_id)

            # Check if the user has already voted using MongoDB query
            already_voted = Post.objects(id=post_id, votes=current_user.id).count()

            if not already_voted:
                post.update(add_to_set__votes=current_user.id)
                return {"message": "Vote recorded successfully by the current user"}, 201
            else:
                return {"message": "User has already voted for this post"}, 200

        except Exception as e:
            return Exception(f"An unexpected error occurred: {str(e)}")

    @jwt_required(fresh=True)
    def delete(self, post_id):
        """
        Remove the vote of the current user from a post.

        Parameters
        ----------
        post_id : str
            The ID of the post.

        Returns
        -------
        dict
            A JSON response indicating the success or failure of the operation.

        Raises
        ------
        Exception
            If an unexpected error occurs during the vote removal process.
        """
        try:
            post = Post.objects.get_or_404(id=post_id)

            # Check if the user has voted before removing using MongoDB query
            has_voted = Post.objects(id=post_id, votes=current_user.id).count()

            if has_voted:
                post.update(pull__votes=current_user.id)
                return {"message": "Vote removed successfully by the current user"}, 204
            else:
                return {"message": "User has not voted for this post"}, 400

        except Exception as e:
            return Exception(f"An unexpected error occurred: {str(e)}")
