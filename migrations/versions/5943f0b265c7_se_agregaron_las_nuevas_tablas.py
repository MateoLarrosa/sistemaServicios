"""Se agregaron las nuevas tablas

Revision ID: 5943f0b265c7
Revises: 878aa015096b
Create Date: 2025-02-05 19:07:19.499950

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '5943f0b265c7'
down_revision = '878aa015096b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clientes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('cuit_cuil', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('telefono', sa.String(length=20), nullable=False),
    sa.Column('calle', sa.String(length=255), nullable=False),
    sa.Column('numero', sa.String(length=10), nullable=False),
    sa.Column('localidad', sa.String(length=100), nullable=False),
    sa.Column('provincia', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cuit_cuil'),
    sa.UniqueConstraint('email')
    )
    op.create_table('locales',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telefono', sa.String(length=20), nullable=True),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('direccion', sa.String(length=255), nullable=False),
    sa.Column('localidad', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('servicios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('estado', sa.String(length=50), nullable=False),
    sa.Column('fecha_creada', sa.DateTime(), nullable=False),
    sa.Column('fecha_finalizada', sa.DateTime(), nullable=True),
    sa.Column('tipo_servicio', sa.String(length=100), nullable=False),
    sa.Column('horario_inicio', sa.DateTime(), nullable=True),
    sa.Column('prioridad', sa.String(length=50), nullable=False),
    sa.Column('repuestos', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tecnicos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('especializacion', sa.String(length=100), nullable=True),
    sa.Column('disponibilidad', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('contrasena', sa.String(length=255), nullable=False),
    sa.Column('tipo_usuario', sa.String(length=50), nullable=False),
    sa.Column('estado', sa.Boolean(), nullable=True),
    sa.Column('ultimo_acceso', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('id_local', sa.Integer(), nullable=True),
    sa.Column('modelo', sa.String(length=50), nullable=True),
    sa.Column('marca', sa.String(length=50), nullable=True),
    sa.Column('logo', sa.String(length=255), nullable=True),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.Column('fue_arreglado', sa.Boolean(), nullable=True),
    sa.Column('numero_serie', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['id_local'], ['locales.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('numero_serie')
    )
    op.create_table('firma_servicio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_servicio', sa.Integer(), nullable=False),
    sa.Column('firma_cliente', sa.String(length=255), nullable=True),
    sa.Column('firma_tecnico', sa.String(length=255), nullable=True),
    sa.Column('fecha_firma', sa.DateTime(), nullable=False),
    sa.Column('confirmacion', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_servicio'], ['servicios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('usuario')
    op.drop_table('servicio')
    op.drop_table('tecnico')
    op.drop_table('cliente')
    op.drop_table('activo')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activo',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.VARCHAR(length=100, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('modelo', sa.VARCHAR(length=50, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('marca', sa.VARCHAR(length=50, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('descripcion', sa.VARCHAR(collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('fue_arreglado', mssql.BIT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='PK__activo__3213E83F84D1A0D9')
    )
    op.create_table('cliente',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.VARCHAR(length=100, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('cuit_cuil', sa.VARCHAR(length=20, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('telefono', sa.VARCHAR(length=20, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('direccion', sa.VARCHAR(length=255, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='PK__cliente__3213E83F59B1C465')
    )
    op.create_table('tecnico',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.VARCHAR(length=100, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('especializacion', sa.VARCHAR(length=100, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('disponibilidad', mssql.BIT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='PK__tecnico__3213E83FDB353DD1')
    )
    op.create_table('servicio',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('estado', sa.VARCHAR(length=50, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('fecha_creacion', sa.DATETIME(), autoincrement=False, nullable=False),
    sa.Column('fecha_finalizacion', sa.DATETIME(), autoincrement=False, nullable=True),
    sa.Column('tipo_servicio', sa.VARCHAR(length=100, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('prioridad', sa.VARCHAR(length=50, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('repuestos', sa.VARCHAR(collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='PK__servicio__3213E83FD4E255AC')
    )
    op.create_table('usuario',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.VARCHAR(length=100, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('contrasena', sa.VARCHAR(length=255, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('tipo_usuario', sa.VARCHAR(length=50, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('estado', mssql.BIT(), autoincrement=False, nullable=True),
    sa.Column('ultimo_acceso', sa.DATETIME(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='PK__usuario__3213E83F94D4965E')
    )
    op.drop_table('firma_servicio')
    op.drop_table('activos')
    op.drop_table('usuarios')
    op.drop_table('tecnicos')
    op.drop_table('servicios')
    op.drop_table('locales')
    op.drop_table('clientes')
    # ### end Alembic commands ###
