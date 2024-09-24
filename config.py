# config.py
import os

class Config:
    SECRET_KEY = 'your_secret_key'  
    SQLALCHEMY_DATABASE_URI = 'postgresql://myuser:mypassword@localhost/sistema_eventos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False