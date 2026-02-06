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
               "data": {
                    "username" : result.username,
                    "fullname" : result.fullname,
                    "email" : result.email
               }
          }), 201
     
@auth_bp.route("/login", methods=["POST"])
def login():     
     data = request.get_json()
     if not data:
          return jsonify({"status": "failed", "message": "No data provided"}), 400

     if not data.get("email") or not data.get("password"):
          missing_fields = []
          if not data.get("email"):
               missing_fields.append("email")
          if not data.get("password"):
               missing_fields.append("password")
          return jsonify({
               "status": "failed",
               "message": f"{', '.join(missing_fields)} is required"
          }), 400

     try:
          result = service.login(email=data["email"], password=data["password"])
          return jsonify({
               "status": "success",
               "data": result
          }), 200

     except ValueError as e:
          return jsonify({"status": "failed", "message": str(e)}), 400

     except Exception as e:
          print(f"Login error: {e}") 
          return jsonify({"status": "failed", "message": "Internal server error"}), 500


          

     