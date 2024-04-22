from flask_restful import Resource, reqparse
from server.app.models.post import Post
from mongoengine.errors import ValidationError, DoesNotExist
from flask_jwt_extended import current_user, jwt_required
from server.app.models.tag import Tag
from server.app.models.user import User
import ast
from flask import request
from bson import ObjectId  # Import ObjectId from bson


parserPost = reqparse.RequestParser()
parserPost.add_argument(
    "title", type=str, location="json", required=True, help="Title cannot be blank"
)
parserPost.add_argument(
    "content", type=str, location="json", required=True, help="Content cannot be blank"
)
parserPost.add_argument(
    "tags", type=list, location="json", required=False, help="Content cannot be blank"
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
    def get(self, post_id=None, tags=None, user_id=None):
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
        try:
            if user_id:
                user = User.objects.get(id=user_id)
                posts = Post.objects(author=user)
                if posts is None:
                    raise DoesNotExist("Post does not exist")
                if tags:
                    posts = posts.filter(tags__in=tags)
                return [post.to_dict() for post in posts]
            elif post_id and post_id is not "tag_filter":
                post = Post.objects(id=post_id).get()
                if post is None:
                    raise DoesNotExist("Post does not exist")
                return post.to_dict()
            else:
                posts = []
                tags = request.args.getlist("tags")
                if request.path == "/feed_posts":
                    for user_id in current_user.following:
                        user = User.objects.get(id=user_id.id)
                        user_posts = Post.objects(author=user)
                        if tags:
                            user_posts = user_posts.filter(tags__in=tags)
                        posts.extend(user_posts)
                elif tags:
                    posts = Post.objects(tags__in=tags)
                else:
                    posts = Post.objects()
                return [post.to_dict() for post in posts]
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 400

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
            tags = []
            for tag in args["tags"]:
                try:
                    assigned_tag = Tag.objects(id=tag).get()
                    tags.append(assigned_tag)
                except:
                    pass
            new_post = Post(
                title=args["title"],
                content=args["content"],
                tags=tags,
                author=current_user,
            )
            new_post.save()
            current_user.update(add_to_set__tags=tags)
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
            if not Post.objects.get(id=post_id):
                return {"error": "Post not found"}, 403
            post = Post.objects.get(id=post_id)
            if post.author.id == current_user.id:
                post.delete()
                return {"message": "Post deleted successfully"}
            else:
                return {"error": "You don't have permission to delete this post"}, 403
        except DoesNotExist:
            return {"error": "Post not found"}, 403
        except ValidationError:
            return {"error": "Post not found"}, 403
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500
