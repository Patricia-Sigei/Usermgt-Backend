import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import psycopg2
from config import Config
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Import routes (to avoid circular imports)
from routes.user_routes import user_bp
from routes.permission_routes import permission_bp

app.register_blueprint(user_bp)
app.register_blueprint(permission_bp)

# Connect to PostgreSQL and manually create tables
def create_tables():
    db_url = os.getenv("DATABASE_URL")
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()
    
    sql_commands = [
        """
        CREATE TABLE IF NOT EXISTS permission (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS "user" (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone_number VARCHAR(20) UNIQUE NOT NULL,
            password VARCHAR(120) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS user_permission (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            permission_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE,
            FOREIGN KEY (permission_id) REFERENCES permission(id) ON DELETE CASCADE
        )
        """
    ]

    for command in sql_commands:
        cursor.execute(command)
    
    connection.commit()
    cursor.close()
    connection.close()

with app.app_context():
    create_tables()  

if __name__ == "__main__":
    app.run(debug=True)