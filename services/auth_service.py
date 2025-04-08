from models import db, Usuario, Cliente
from flask_jwt_extended import create_access_token
from datetime import datetime

def register_user(data):
    """Registra un nuevo usuario y su cliente asociado."""

    # Verificar si el nombre de usuario ya existe
    if Usuario.query.filter_by(username=data["username"]).first():
        return {"message": "El nombre de usuario ya existe"}, 400

    # Crear el nuevo usuario
    new_user = Usuario(
        username=data["username"],
        email=data["email"],  # El email ya no requiere verificar duplicados
        rol=data.get("rol", "usuario")  # opcional, por defecto "usuario"
    )
    new_user.set_password(data["password"])

    # Agregar el usuario a la sesión
    db.session.add(new_user)
    db.session.flush()  # para conseguir el ID antes del commit

    # Intentar parsear la fecha de nacimiento
    try:
        fecha_nacimiento = datetime.strptime(data["fecha_nacimiento"], "%Y-%m-%d").date()
    except ValueError:
        return {"message": "Formato de fecha inválido. Usa YYYY-MM-DD."}, 400

    # Crear el cliente asociado al usuario
    new_cliente = Cliente(
        nombre=data["nombre"],
        apellidos=data["apellidos"],
        fecha_nacimiento=fecha_nacimiento,
        usuario_id=new_user.id
    )

    # Agregar el cliente a la sesión
    db.session.add(new_cliente)

    # Confirmar los cambios en la base de datos
    db.session.commit()

    return {"message": "Usuario y cliente registrados correctamente"}, 201

def login_user(data):
    """Autentica al usuario y devuelve un token JWT basándose en el nombre de usuario."""
    user = Usuario.query.filter_by(username=data["username"]).first()

    if user and user.check_password(data["password"]):
        token = create_access_token(identity=str(user.id))
        return {"access_token": token, "nombre": user.username, "rol": user.rol}, 200

    return {"message": "Credenciales incorrectas"}, 401
