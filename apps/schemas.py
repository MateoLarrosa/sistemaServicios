from marshmallow import Schema, fields, validate

class ClienteSchema(Schema):
    id = fields.Int(dump_only = True) # solo lectura
    nombre = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    cuit_cuil = fields.Str(required=True, validate=validate.Length(equal=13))  # "XX-XXXXXXXX-X"
    email = fields.Email(required=True)
    telefono = fields.Str(required=True, validate=validate.Length(min=7, max=15))
    direccion = fields.Str(required=True)

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)