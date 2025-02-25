from flask import Blueprint, request, jsonify
from models import db, User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

user_bp = Blueprint('user_bp', __name__, url_prefix='/users')

# Create a new user
@user_bp.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
    permissions = data.get('permissions', [])  
    
    new_user = User(name=name, email=email, phone_number=phone_number, password=password, permissions=permissions)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User created successfully", "user": new_user.to_dict()}), 201

# Get all users
@user_bp.route('/all', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# Get a specific user by ID
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

# Update a user
@user_bp.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.phone_number = data.get('phone_number', user.phone_number)
    if 'password' in data:
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user.permissions = data.get('permissions', user.permissions)
    
    db.session.commit()
    return jsonify({"message": "User updated successfully", "user": user.to_dict()}), 200

# Delete a user
@user_bp.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
