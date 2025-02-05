from flask import Blueprint, request, jsonify
from database import db
from models import Cliente

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/clientes', methods=['GET'])
def obtener_clientes():
    clientes = Cliente.query.all()
    return jsonify([{
        "id": cliente.id,
        "nombre": cliente.nombre,
        "cuit_cuil": cliente.cuit_cuil,
        "email": cliente.email,
        "telefono": cliente.telefono,
        "direccion": cliente.direccion
    } for cliente in clientes]), 200

@cliente_bp.route('/clientes', methods=['POST'])
def crear_cliente():
    data = request.get_json()
    nuevo_cliente = Cliente(
        nombre=data.get('nombre'),
        cuit_cuil=data.get('cuit_cuil'),
        email=data.get('email'),
        telefono=data.get('telefono'),
        direccion=data.get('direccion')
    )
    db.session.add(nuevo_cliente)
    db.session.commit()
    return jsonify({"message": "Cliente creado exitosamente"}), 201

@cliente_bp.route('/clientes/<int:id>', methods=['PUT'])
def actualizar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    data = request.get_json()
    cliente.nombre = data.get('nombre', cliente.nombre)
    cliente.cuit_cuil = data.get('cuit_cuil', cliente.cuit_cuil)
    cliente.email = data.get('email', cliente.email)
    cliente.telefono = data.get('telefono', cliente.telefono)
    cliente.direccion = data.get('direccion', cliente.direccion)

    db.session.commit()
    return jsonify({"message": "Cliente actualizado exitosamente"}), 200

@cliente_bp.route('/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"message": "Cliente eliminado exitosamente"}), 200
