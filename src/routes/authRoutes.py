from flask import Blueprint, request, jsonify
from ..services import AuthService

auth_bp = Blueprint("auth",__name__)
service = AuthService()

@auth_bp.route("/register", methods=["POST"])
def register():
     data = request.get_json()
     username = data["username"]
     fullname = data["fullname"]
     email = data["email"]
     password = data["password"]

     service.register(username=username,fullname=fullname,email=email,password=password)
     return jsonify({
          "message" : "succes"
     })