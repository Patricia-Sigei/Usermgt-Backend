from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import db, User, Role
from schemas.user import user_schema, users_schema

bcrypt = Bcrypt()
# jwt = JWTManager()
user_bp = Blueprint("users", __name__)

# Create a new user (Admin only)
@user_bp.route("/create", methods=["POST"])
@jwt_required()
def create_user():
    current_user_id = get_jwt_identity()
    admin = User.query.get(current_user_id)
    if not admin or admin.role_id != 1:
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    phone_number = data.get("phone_number")
    password = data.get("password")
    role_id = data.get("role_id")

    if not all([name, email, phone_number, password, role_id]):
        return jsonify({"error": "All fields are required"}), 400
    
    existing_user = User.query.filter((User.email == email) | (User.phone_number == phone_number)).first()
    if existing_user:
        return jsonify({"error": "Email or phone number already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(
        name=name, 
        email=email, 
        phone_number=phone_number, 
        password=hashed_password, 
        role_id=role_id
    )
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify(user_schema.dump(new_user)), 201

# Get all users (Admin only)
@user_bp.route("/all", methods=["GET"])
@jwt_required()
def get_users():
    current_user_id = get_jwt_identity()
    admin = User.query.get(current_user_id)
    if not admin or admin.role_id != 1:
        return jsonify({"error": "Admin access required"}), 403

    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200

# Get a single user by ID
@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"error": "Unauthorized access"}), 403
    
    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user)), 200

# Update user by ID
@user_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"error": "Unauthorized access"}), 403
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    user.phone_number = data.get("phone_number", user.phone_number)
    user.password = bcrypt.generate_password_hash(data.get("password", user.password)).decode("utf-8")
    user.role_id = data.get("role_id", user.role_id)
    
    db.session.commit()
    return jsonify(user_schema.dump(user)), 200

# Delete a user (Admin only)
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    admin = User.query.get(current_user_id)
    if not admin or admin.role_id != 1:
        return jsonify({"error": "Admin access required"}), 403
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
