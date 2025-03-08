import re
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify, request, redirect, url_for
from apps.database import db
from apps.models import Auditoria, CasoAuditoria
from datetime import datetime


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



def validar_mail(mail):
    """Valida que el mail tenga un formato correcto"""
    patron = r"[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron,mail)

def validar_cuit(cuil):

    """Valida que el CUIT tenga el formato correcto(11 numeros sin guiones)"""
    return re.match(r"\d{11}", cuil)


def cargar_casos_auditoria():
    
    casos = [
        "Inicio de sesión exitoso",
        "Intento de login fallido",
        "Creación de un nuevo cliente",
        "Eliminación de un cliente",
        "Actualización de un cliente",
        "Actualización de un técnico",
    ]
    for descripcion in casos:
        if not CasoAuditoria.query.filter_by(descripcion=descripcion).first():
            db.session.add(CasoAuditoria(descripcion=descripcion))
    
    db.session.commit()


def registrar_evento_auditoria(id_caso, id_usuario=None, id_cliente=None, id_tecnico=None, detalle=None):
    """
    Registra un evento en la tabla Auditoria.

    :param id_caso: ID del tipo de evento en la tabla CasoAuditoria
    :param id_usuario: ID del usuario que generó la acción (opcional)
    :param id_cliente: ID del cliente afectado (opcional)
    :param id_tecnico: ID del técnico afectado (opcional)
    :param detalle: Información adicional sobre la acción realizada (opcional)
    :param direccion_IP: Obtengo la direccion IP de donde vino la solicitud
    """
    nuevo_evento = Auditoria(
        id_caso= id_caso,
        id_usuario=id_usuario,
        id_cliente=id_cliente,
        id_tecnico=id_tecnico,
        fecha_evento=datetime.utcnow(),
        detalle=detalle,
        direccionIP = str(request.remote_addr)
    )
    db.session.add(nuevo_evento)
    db.session.commit()

    ## RUTA PARA CARGAR LOGOS -----------------------------------------------------------------------------------------------

