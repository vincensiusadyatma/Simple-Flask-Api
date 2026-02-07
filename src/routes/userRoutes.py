from flask import Blueprint, request, jsonify, g
from ..services import UserService, OrderService
from ..middlewares.token_required import token_required

user_bp = Blueprint("user", __name__, url_prefix="/users")
service = UserService()


@user_bp.route("/")
@token_required
def list_users():
    try:
        current_user = g.user
        users = service.list_users()
        return jsonify({
            "status": "success",
            "users": [
                {"id": u.id, "username": u.username, "fullname": u.fullname, "email": u.email} 
                for u in users
            ]
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@user_bp.route("/<int:user_id>")
@token_required
def get_user(user_id):
    try:
        current_user = g.user
        u = service.get_user(user_id)
        if not u:
            return jsonify({"status": "error", "message": "User not found"}), 404
        return jsonify({
            "status": "success",
            "user": current_user.username,
            "data": {"id": u.id, "username": u.username, "fullname": u.fullname, "email": u.email}
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@user_bp.route("/", methods=["POST"])
@token_required
def create_user():
    try:
        data = request.json
        required_fields = ["username", "fullname", "email", "password"]
        if not all(field in data and data[field] for field in required_fields):
            return jsonify({"status": "error", "error": "Missing fields"}), 400

        u = service.create_user(
            username=data["username"],
            fullname=data["fullname"],
            email=data["email"],
            password=data["password"]
        )
        if not u:
            return jsonify({"status": "error", "error": "Failed to create user"}), 500

        return jsonify({"status": "success", "message": f"User {u.username} created"}), 201
    except ValueError as ve:
        return jsonify({"status": "error", "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@user_bp.route("/<int:user_id>", methods=["PUT"])
@token_required
def update_user(user_id):
    try:
        data = request.json
        u = service.update_user(user_id, data)
        if not u:
            return jsonify({"status": "error", "error": "User not found"}), 404
        return jsonify({"status": "success", "message": f"User {u.username} updated"}), 200
    except ValueError as ve:
        return jsonify({"status": "error", "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@user_bp.route("/<int:user_id>", methods=["DELETE"])
@token_required
def delete_user(user_id):
    try:
        u = service.delete_user(user_id)
        if not u:
            return jsonify({"status": "error", "error": "User not found"}), 404
        return jsonify({"status": "success", "message": f"User {u.username} deleted"}), 200
    except ValueError as ve:
        return jsonify({"status": "error", "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
