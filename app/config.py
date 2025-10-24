import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL')
    PORT = int(os.getenv('PORT', 8000))
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    @staticmethod
    def validate():
        if not Config.DATABASE_URL:
            raise ValueError("DATABASE_URL n'est pas définie dans les variables d'environnement")
        if Config.FLASK_ENV == 'production' and Config.SECRET_KEY == 'dev-secret-key':
            raise ValueError("SECRET_KEY doit être définie en production")
