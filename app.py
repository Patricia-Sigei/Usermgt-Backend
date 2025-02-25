import os
import psycopg2
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Import database and schema serializer (db is already initialized in models/__init__.py )
from models import db  
from schemas import ma

# Initialize database and schema serializer
db.init_app(app)
ma.init_app(app)

# Import and register blueprints
from routes.user import user_bp

app.register_blueprint(user_bp)

# Function to manually create PostgreSQL tables
def create_tables():
    try:
        connection = psycopg2.connect(Config.SQLALCHEMY_DATABASE_URI)
        cursor = connection.cursor()

        sql_commands = [
            """
            CREATE TABLE IF NOT EXISTS "user" (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone_number VARCHAR(20) UNIQUE NOT NULL,
                password VARCHAR(120) NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE,
                permissions TEXT[] DEFAULT ARRAY[]::TEXT[]
            )
            """
        ]

        for command in sql_commands:
            cursor.execute(command)

        connection.commit()
        print("Tables created successfully!")

    except Exception as e:
        print(f"Error creating tables: {e}")

    finally:
        cursor.close()
        connection.close()

# Run table creation in the app context
with app.app_context():
    create_tables()

if __name__ == "__main__":
    app.run(debug=True)
