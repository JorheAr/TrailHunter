from flask import request, jsonify
from services.auth_service import register_user, login_user
from flask_jwt_extended import jwt_required

def register():
    """Controlador para el registro de usuario."""
    data = request.get_json()
    return jsonify(*register_user(data))

def login():
    """Controlador para el inicio de sesión."""
    data = request.get_json()
    return jsonify(*login_user(data))

@jwt_required()
def protected():
    """Ruta protegida para probar JWT."""
    return jsonify({"message": "Acceso permitido"}), 200
