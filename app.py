from flask import Flask
from flask_bcrypt import Bcrypt  
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS  
from config import Config
from models import db
from routes.user import user_bp
from routes.auth import auth_bp
from routes.role import role_bp
from routes.permissions import permission_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 1209600

# initialize Bcrypt
# bcrypt = Bcrypt(app)  
# allowing all apps to use access the routes
CORS(app, resources={r"/*": {"origins": "*"}})  

# Initialize other extensions
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)  


# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(role_bp)
app.register_blueprint(permission_bp)

# Create tables using Flask-Migrate
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
