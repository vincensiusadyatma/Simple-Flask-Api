from flask import Blueprint, request, jsonify
from ..services import AuthService

auth_bp = Blueprint("auth",__name__)
service = AuthService()

@auth_bp.route("/register", methods=["POST"])
def register():
     data = request.get_json()
  
     try:
          username = data["username"]
          fullname = data["fullname"]
          email = data["email"]
          password = data["password"]

          result = service.register(
               username=username,
               fullname=fullname,
               email=email,
               password=password
          )

     except KeyError as e:
          return jsonify({
          "status": "failed",
          "message": f"{e.args[0]} is required"
     }), 400

     except ValueError as e:
          return jsonify({
               "status": "failed",
               "message": str(e)
          }), 400

     except Exception as e:
          return jsonify({
               "status": "failed",
               "message": "Internal server error"
          }), 500
     
     else:
          return jsonify({
               "status": "success",
               "data": result
          }), 201
