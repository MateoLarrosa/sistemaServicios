import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://@MSI\\SQLEXPRESS/sistemaServicioTecnico?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'prueba12345')

