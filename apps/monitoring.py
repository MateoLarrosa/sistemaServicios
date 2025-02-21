import psutil
import time
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.models import Usuario

monitoreo_bp = Blueprint('monitoreo', __name__)

# Diccionario para rastrear usuarios activos
usuarios_activos = {}

# Tiempo límite para considerar un usuario como activo (en segundos)
TIEMPO_USUARIO_ACTIVO = 300  # 5 minutos

@monitoreo_bp.route('/monitoreo', methods=['GET'])

@jwt_required()
def obtener_monitoreo():
    """ Devuelve el estado actual del sistema y el número de usuarios activos. """
    usuario_id = get_jwt_identity()

     # Obtener el usuario desde la base de datos
    usuario = Usuario.query.get(usuario_id)

    # Verificar si el usuario es "mateoAdmin"
    if usuario.nombreUsuario != "mateoAdmin":
        return jsonify({"error": "Acceso no autorizado."}), 403


    tiempo_actual = time.time()
    
    # Registrar al usuario como activo
    global usuarios_activos
    usuarios_activos[usuario_id] = tiempo_actual

    # Limpiar usuarios inactivos
    usuarios_activos_filtrados = {
        user: last_seen for user, last_seen in usuarios_activos.items()
        if tiempo_actual - last_seen < TIEMPO_USUARIO_ACTIVO
    }

    # Actualizar la lista de usuarios activos
    usuarios_activos = usuarios_activos_filtrados

    # Obtener métricas del sistema
    uso_cpu = psutil.cpu_percent(interval=1)
    uso_memoria = psutil.virtual_memory().percent
    cantidad_usuarios_activos = len(usuarios_activos)

    return jsonify({
        "cpu_percent": uso_cpu,
        "ram_percent": uso_memoria,
        "usuarios_activos": cantidad_usuarios_activos
    }), 200
