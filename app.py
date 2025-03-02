from flask import Flask
from flask_bcrypt import Bcrypt  # ✅ Import correctly
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
from models import db
from schemas import ma
from routes.user import user_bp
from routes.auth import auth_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# initialize Bcrypt
bcrypt = Bcrypt(app)  

# Initialize other extensions
db.init_app(app)
ma.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)  

# Register blueprints
app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(auth_bp, url_prefix="/auth")

# Create tables using Flask-Migrate
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
