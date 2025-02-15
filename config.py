import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY','b4d7e8f9h10a11b12b12c13c14e14f15a22b21c20d19e18f17')
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://@MSI\\SQLEXPRESS/sistemaServicioTecnico?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '$2b$12$YSi0BHH8Hf6DS3no4.q8me7XodOFydFY/KKopNHiRv.wr3xVgdvke')
    

