from flask import Blueprint, request, jsonify
from models import db
from models.role import Role  

role_bp = Blueprint("role_bp", __name__)

# Route to Add a New role and its permissions
@role_bp.route("/roles", methods=["POST"])
def create_role():
    data = request.get_json()
    
    if not data or not data.get("name") or not isinstance(data.get("permissions", []), list):
        return jsonify({"error": "Invalid input"}), 400

    existing_role = Role.query.filter_by(name=data["name"]).first()
    if existing_role:
        return jsonify({"error": "Role already exists"}), 409

    new_role = Role(
        name=data["name"],
        permissions=data["permissions"]
    )

    db.session.add(new_role)
    db.session.commit()

    return jsonify({"message": "Role created successfully", "role": new_role.to_dict()}), 201

# Route to Get All Roles
@role_bp.route("/roles", methods=["GET"])
def get_roles():
    roles = Role.query.all()
    return jsonify([role.to_dict() for role in roles]), 200

# Route to Get a Single Role by ID
@role_bp.route("/roles/<int:role_id>", methods=["GET"])
def get_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404
    return jsonify(role.to_dict()), 200

# Route to Update Permissions for a Role
@role_bp.route("/roles/<int:role_id>/permissions", methods=["PUT"])
def update_role_permissions(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404

    data = request.get_json()
    if not isinstance(data.get("permissions", []), list):
        return jsonify({"error": "Invalid permissions format"}), 400

    role.permissions = list(set(data["permissions"])) 
    db.session.commit()

    return jsonify({"message": "Permissions updated", "role": role.to_dict()}), 200

# Route to Add a New Permission to an Existing Role
@role_bp.route("/roles/<int:role_id>/add_permission", methods=["POST"])
def add_permission(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404

    data = request.get_json()
    permission = data.get("permission")

    if not permission or not isinstance(permission, str):
        return jsonify({"error": "Invalid permission format"}), 400

    if permission not in role.permissions:
        role.permissions.append(permission)
        role.permissions = list(set(role.permissions)) 
        db.session.commit()

    return jsonify({"message": "Permission added", "role": role.to_dict()}), 200

# Route to Remove a Permission from a Role
@role_bp.route("/roles/<int:role_id>/remove_permission", methods=["POST"])
def remove_permission(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404

    data = request.get_json()
    permission = data.get("permission")

    if not permission or not isinstance(permission, str):
        return jsonify({"error": "Invalid permission format"}), 400

    if permission in role.permissions:
        role.permissions.remove(permission)
        db.session.commit()

    return jsonify({"message": "Permission removed", "role": role.to_dict()}), 200

# Route to Delete a Role
@role_bp.route("/roles/<int:role_id>", methods=["DELETE"])
def delete_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404

    db.session.delete(role)
    db.session.commit()

    return jsonify({"message": "Role deleted successfully"}), 200
