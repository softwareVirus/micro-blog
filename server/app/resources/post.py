from flask_restful import Resource, reqparse
from models.post import Post
from flask_jwt_extended import current_user, jwt_required
import ast


parserPost = reqparse.RequestParser()
parserPost.add_argument(
    "title", type=str, location="json", required=True, help="Title cannot be blank"
)
parserPost.add_argument(
    "content", type=str, location="json", required=True, help="Content cannot be blank"
)


class PostResource(Resource):
    """
    A resource for managing posts.

    Attributes
    ----------
    parserPost : reqparse.RequestParser
        Request parser for handling post-related data.

    Methods
    -------
    get()
        Retrieve all posts.

    post()
        Create a new post.

    delete(post_id)
        Delete a post.
    """

    @jwt_required(fresh=True)
    def get(self, post_id=None):
        """
        Retrieve all posts.

        Returns
        -------
        list
            List of dictionaries representing posts.

        Raises
        ------
        Exception
            If an unexpected error occurs while retrieving posts.
        """
        if post_id:
            post = Post.objects(id=post_id).get()
            return post.to_dict()
        else:
            posts = Post.objects()
            return [post.to_dict() for post in posts]

    @jwt_required(fresh=True)
    def post(self):
        """
        Create a new post.

        Returns
        -------
        dict
            Dictionary representing the newly created post.
        int
            HTTP status code indicating the success of the operation.

        Raises
        ------
        Exception
            If an unexpected error occurs while creating a post.
        """
        try:
            args = parserPost.parse_args()

            new_post = Post(
                title=args["title"],
                content=args["content"],
                author=current_user,
            )
            new_post.save()
            post_dict = new_post.to_dict()

            return post_dict, 201
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 400

    @jwt_required(fresh=True)
    def delete(self, post_id):
        """
        Delete a post.

        Parameters
        ----------
        post_id : str
            The ID of the post to be deleted.

        Returns
        -------
        dict
            Dictionary indicating the success of the delete operation.
        int
            HTTP status code indicating the success of the operation.

        Raises
        ------
        Post.DoesNotExist
            If the specified post is not found.
        Exception
            If an unexpected error occurs while deleting a post.
        """

        try:
            post = Post.objects.get(id=post_id)

            if post.author.id == current_user.id:
                post.delete()
                return {"message": "Post deleted successfully"}
            else:
                return {"error": "You don't have permission to delete this post"}, 403
        except Post.DoesNotExist:
            return {"error": "Post not found"}, 404
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500
