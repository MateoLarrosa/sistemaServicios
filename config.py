import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY','b4d7e8f9h10a11b12b12c13c14e14f15a22b21c20d19e18f17')
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://@MSI\\SQLEXPRESS/sistemaServicioTecnico?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'a5c6d7e8f9b10a11b12c13d14e15f16a17b18c19d20e21f22')
    

