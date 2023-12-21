from flask import request
from flask_restful import Resource, reqparse
from models.post import Post
from models.comment import Comment
from flask_jwt_extended import current_user, jwt_required

parserComment = reqparse.RequestParser()
parserComment.add_argument(
    "content", type=str, required=True, help="Content cannot be blank"
)


class CommentResource(Resource):
    """
    A resource for managing comments on a post.

    Attributes
    ----------
    parserComment : reqparse.RequestParser
        Request parser for handling comment-related data.

    Methods
    -------
    post(post_id, parent_comment_id=None)
        Add a new comment to a post.

    get(post_id, comment_id=None)
        Retrieve comments for a post.

    delete(post_id, comment_id)
        Delete a comment from a post.
    """

    @jwt_required()
    def post(self, post_id, parent_comment_id=None):
        """
        Add a new comment to a post.

        Parameters
        ----------
        post_id : str
            The ID of the post to which the comment will be added.
        parent_comment_id : str, optional
            The ID of the parent comment if the comment is a reply.

        Returns
        -------
        dict
            A dictionary representing the newly created comment.
        int
            HTTP status code indicating the success of the operation.

        Raises
        ------
        Comment.DoesNotExist
            If the specified comment or post is not found.
        Exception
            If an unexpected error occurs during the operation.
        """
        try:
            post = Post.objects.get(id=post_id)

            if current_user is None:
                return {"error": "User not found"}, 404

            args = parserComment.parse_args()
            new_comment = Comment(
                content=args["content"],
                author=current_user,
            )

            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                new_comment.parent_comment = parent_comment
            new_comment.save()
            post.comments.append(new_comment)
            post.save()
            return new_comment.to_dict(), 201

        except Comment.DoesNotExist:
            return {"error": "Comment not found"}, 404
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500

    @jwt_required()
    def get(self, post_id, comment_id=None):
        """
        Retrieve comments for a post.

        Parameters
        ----------
        post_id : str
            The ID of the post for which comments are retrieved.
        comment_id : str, optional
            The ID of a specific comment to retrieve.

        Returns
        -------
        list or dict
            A list of parent comments or a dictionary representing a specific comment.
        int
            HTTP status code indicating the success of the operation.

        Raises
        ------
        Comment.DoesNotExist
            If the specified comment or post is not found.
        Exception
            If an unexpected error occurs during the operation.
        """
        try:
            post = Post.objects.get(id=post_id)

            if comment_id:
                # Retrieve a specific comment by ID
                comment = Comment.objects.get(id=comment_id)
                return comment.to_dict(), 200
            else:
                # Retrieve parent comments (comments without a parent)
                parent_comments = [
                    comment.to_dict()
                    for comment in post.comments
                    if not comment.parent_comment
                ]

                return parent_comments, 200

        except Comment.DoesNotExist:
            return {"error": "Comment not found"}, 404
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500

    @jwt_required()
    def delete(self, post_id, comment_id):
        """
        Delete a comment from a post.

        Parameters
        ----------
        post_id : str
            The ID of the post from which the comment will be deleted.
        comment_id : str
            The ID of the comment to be deleted.

        Returns
        -------
        dict
            A message indicating the success of the delete operation.

        Raises
        ------
        Comment.DoesNotExist
            If the specified comment or post is not found.
        Exception
            If an unexpected error occurs during the operation.
        """
        try:
            post = Post.objects.get(id=post_id)

            if current_user is None:
                return {"error": "User not found"}, 404

            comment = Comment.objects.get(id=comment_id)

            if comment.author.id == current_user.id:
                post.comments.remove(comment)
                post.save()

                comment.delete()
                return {"message": "Comment deleted successfully"}
            else:
                return {
                    "error": "You don't have permission to delete this comment"
                }, 403

        except Comment.DoesNotExist:
            return {"error": "Comment not found"}, 404
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500
