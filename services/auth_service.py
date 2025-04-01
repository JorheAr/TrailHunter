from models import db, Usuario
from flask_jwt_extended import create_access_token


def register_user(data):
    """Registra un nuevo usuario en la base de datos."""
    if Usuario.query.filter_by(email=data["email"]).first():
        return {"message": "El usuario ya existe"}, 400

    new_user = Usuario(nombre=data["nombre"], email=data["email"])
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()
    return {"message": "Usuario registrado correctamente"}, 201


def login_user(data):
    """Autentica al usuario y devuelve un token JWT."""
    user = Usuario.query.filter_by(email=data["email"]).first()

    if user and user.check_password(data["password"]):
        token = create_access_token(identity=user.id)
        return {"access_token": token}, 200

    return {"message": "Credenciales incorrectas"}, 401
