from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

auth_bp = Blueprint("auth", __name__)
# Login routes that makes use of JWT
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    name = data.get("name")
    password = data.get("password")

    user = User.query.filter_by(name=name).first()

    if not user:
        print("User not found")
        return jsonify({"error": "Invalid name or password"}), 401

    # print(f"Stored Hash: {user.password}")
    # print(f"Input Password: {password}") (debug not necessary)

    if not bcrypt.check_password_hash(user.password, password):
        print("Password check failed")
        return jsonify({"error": "Invalid name or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token, "message": "Login successful"}), 200


# route to reset password - requires the JWT TOKEN FOR Resetting (every user can reset their own password)

@auth_bp.route("/reset-password", methods=["POST"])
@jwt_required()
def reset_password():
    data = request.get_json()
    new_password = data.get("new_password")

    # Get the logged-in user from the JWT token (It will use the user ID)
    user_id = get_jwt_identity()
    user = User.query.get(user_id) 

    if not user:
        return jsonify({"error": "User not found"}), 404

    hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
    user.password = hashed_password
    db.session.commit()

    return jsonify({"message": "Password reset successful"}), 200

