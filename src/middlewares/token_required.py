from functools import wraps
from flask import request, jsonify, g
import jwt
from ..config import Config
from ..repositories import AuthRepository

auth_repo = AuthRepository()

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"message": "Token is missing"}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"message": "Invalid token format"}), 401

        token = parts[1]

        try:
            payload = jwt.decode(token, Config.SECRET, algorithms=["HS256"])
            username = payload.get("username")
            email = payload.get("email")

            user_by_username = auth_repo.get_user_by_username(username)
            user_by_email = auth_repo.getUserByEmail(email) 

            if not user_by_username or not user_by_email:
                return jsonify({"message": "User not found"}), 401

            g.user = user_by_username

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return func(*args, **kwargs)

    return wrapper
