from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify

def admin_required(fn):
    """Restringe el acceso solo a usuarios administradores."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()  # 🔥 Ahora obtenemos todos los datos del token
        print(f'claims del token{claims}')
        
        if claims.get("tipoUsuario").lower() != "admin":  # 🔥 Comprobamos el tipo de usuario
            return jsonify({"error": "Acceso no autorizado"}), 403  # Código HTTP 403: Forbidden
        
        return fn(*args, **kwargs)
    
    return wrapper


