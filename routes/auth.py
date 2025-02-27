from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from models import db, User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

auth_bp = Blueprint("auth", __name__)
# Login routes that makes use of JWT
@auth_bp.route("/login", methods=["POST"])
@jwt_required()
def login():
    data = request.get_json()
    name = data.get("name")
    password = data.get("password")

    user = User.query.filter_by(name=name).first()
    
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid name or password"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token, "message": "Login successful"}), 200

# route to reset password
@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data.get("email")
    new_password = data.get("new_password")

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.password = hashed_password
    db.session.commit()
    
    return jsonify({"message": "Password reset successful"}), 200
