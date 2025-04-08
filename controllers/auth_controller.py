from flask import request, jsonify
from services.auth_service import register_user, login_user
from flask_jwt_extended import jwt_required, get_jwt_identity


def register():
    data = request.get_json()
    response, status_code = register_user(data)
    return jsonify(response), status_code

def login():
    data = request.get_json()
    response, status_code = login_user(data)
    return jsonify(response), status_code

@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({"message": f"Acceso concedido para el usuario con ID {current_user_id}"}), 200
