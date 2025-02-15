from marshmallow import Schema, fields, validate

class ClienteSchema(Schema):
    d = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    cuit = fields.Str(required=True)  # 🔄 Antes era 'cuit_cuil'
    mail = fields.Email(required=True)  # 🔄 Antes era 'email'
    telefono = fields.Str(required=True)
    calle = fields.Str(required=True)  # 🔄 Agregado
    numero = fields.Str(required=True)  # 🔄 Agregado
    direccion = fields.Str()  # ❌ Opcional
    localidad = fields.Str(required=True)
    provincia = fields.Str(required=True)
    latitud = fields.Float()
    longitud = fields.Float()
    idUsuario = fields.Int()
    razonSocial = fields.Str(required=True)

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)