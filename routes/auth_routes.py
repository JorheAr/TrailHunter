from flask import Blueprint
from controllers.auth_controller import register, login, protected

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/register", methods=["POST"])(register)
auth_bp.route("/login", methods=["POST"])(login)
auth_bp.route("/protected", methods=["GET"])(protected)
