import psycopg2
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from schemas import ma
from routes.user import user_bp
from routes.auth import auth_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db.init_app(app)
ma.init_app(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(auth_bp, url_prefix="/auth")

# Function to create tables
def create_tables():
    try:
        connection = psycopg2.connect(Config.SQLALCHEMY_DATABASE_URI)
        cursor = connection.cursor()

        sql_commands = [
            # deleting the old table
            """DROP TABLE IF EXISTS "user", roles CASCADE""",  
            """
            CREATE TABLE roles (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL,
                permissions TEXT[] DEFAULT ARRAY[]::TEXT[]
            )
            """,
            """
            CREATE TABLE "user" (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone_number VARCHAR(20) UNIQUE NOT NULL,
                password_hash VARCHAR(120) NOT NULL,
                role_id INTEGER REFERENCES roles(id) ON DELETE SET NULL
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

# Create tables on app start
with app.app_context():
    create_tables()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
