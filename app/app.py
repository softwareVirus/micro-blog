from flask import Flask
from flask_restful import Api
import os
from mongoengine import connect
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from models.user import User
from resources.auth import LoginResource, SignupResource
from resources.protected import Profile
from flask_cors import CORS

load_dotenv()  # take environment variables from .env.

# Connect to MongoDB using the provided connection string
connect(host=os.getenv("MONGODB_CONNECTION_STRING"))

app = Flask(__name__)
CORS(app)
api = Api(app)

# Set the JWT secret key, load from environment variable for security
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret_key")
jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_loader(user):
    """Callback function to get the identity of the current user."""
    return str(user.id)

@jwt.user_lookup_loader
def user_lookup_loader(_jwt_header, jwt_data):
    """Callback function to look up a user by identity in JWT data."""
    identity = jwt_data["sub"]
    return User.objects.get(id=identity)

# Define API routes and associate them with the respective resources
api.add_resource(SignupResource, "/signup")
api.add_resource(LoginResource, "/login")
api.add_resource(Profile, "/profile")

if __name__ == '__main__':
    # Run the Flask application in debug mode during development
    app.run(debug=True)
