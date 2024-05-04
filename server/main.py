from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from mongoengine import connect
import mongomock
import os
from dotenv import load_dotenv
from server.app.api.routes import routes_bp
from server.util.jwt_conf import jwt, JWTConfig
from server.app.socket import socketio
load_dotenv()  # Load environment variables from .env.


def create_db_connection(mode="dev"):
    # with open(f"./config.json", "r") as f:
    #    config = json.load(f)

    if mode == "dev":
        connect(
            host=os.getenv("MONGODB_CONNECTION_STRING")
        )  # host=config["dev"]["MONGODB_URI"])
    if mode == "test":
        connect(
            "mongoenginetest",
            host="mongodb://localhost",
            mongo_client_class=mongomock.MongoClient,
            uuidRepresentation="standard",
        )

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
app.config.from_object(JWTConfig)

app.register_blueprint(routes_bp)
jwt.init_app(app)
socketio.init_app(app, cors_allowed_origins="*")

create_db_connection("dev")

if __name__ == "__main__":
    # Run the Flask application in debug mode during development
    socketio.run(app, host="0.0.0.0", debug=True)

