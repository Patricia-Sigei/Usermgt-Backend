from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from models import User, Role

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.role or user.role.name.lower() != "admin":
            return jsonify({"error": "Admin access required"}), 403

        return fn(*args, **kwargs)

    return wrapper
