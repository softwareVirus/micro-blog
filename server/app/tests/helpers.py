import bcrypt
from app.models.user import User
import uuid

signup_data = {
    "email": f"test{uuid.uuid4()}@example.com",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User",
}


def generate_hashed_password():
    salt = bcrypt.gensalt(16)
    hashed_password = bcrypt.hashpw(str.encode(signup_data["password"]), salt=salt)
    return hashed_password


def create_user():
    try:
        hashed_password = generate_hashed_password()
        user = User.objects.create(
            first_name=signup_data["first_name"],
            last_name=signup_data["last_name"],
            email=f"test{uuid.uuid4()}@example.com",
            hashed_password=hashed_password,
        )
        return user
    except Exception as e:
        return {"error": e}, 500


def create_mock_user():
    try:
        hashed_password = generate_hashed_password()
        user = User(
            first_name=signup_data["first_name"],
            last_name=signup_data["last_name"],
            email=f"test{uuid.uuid4()}@example.com",
            hashed_password=hashed_password,
        )
        return user
    except Exception as e:
        return {"error": e}, 500
