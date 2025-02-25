import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Secret Key 
    SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    
    # PostgreSQL Database Configuration
    DB_CONFIG = {
        "dbname": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("DB_PORT")
    }

    # SQLAlchemy Database URI for PostgreSQL
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
