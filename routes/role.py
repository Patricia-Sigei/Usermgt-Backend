from flask import Blueprint, request, jsonify
from models import db
from models.role import Role
from models.permissions import Permission

role_bp = Blueprint("role_bp", __name__)

# Create a new role with assigned permissions
@role_bp.route("/new-roles", methods=["POST"])
def create_role():
    data = request.get_json()

    if not data or not data.get("name") or not isinstance(data.get("permissions", []), list):
        return jsonify({"error": "Invalid input"}), 400

    existing_role = Role.query.filter_by(name=data["name"]).first()
    if existing_role:
        return jsonify({"error": "Role already exists"}), 409

    permissions = Permission.query.filter(Permission.id.in_(data["permissions"])).all()
    new_role = Role(name=data["name"], permissions=permissions)

    db.session.add(new_role)
    db.session.commit()

    return jsonify({"message": "Role created successfully", "role": new_role.to_dict()}), 201

# Get all roles
@role_bp.route("/all-roles", methods=["GET"])
def get_roles():
    roles = Role.query.all()
    return jsonify([role.to_dict() for role in roles]), 200

# Get a single role by ID
@role_bp.route("/one-role/<int:role_id>", methods=["GET"])
def get_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404
    return jsonify(role.to_dict()), 200

# Update a role (name & permissions)
@role_bp.route("/update-role/<int:role_id>", methods=["PUT"])
def update_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404

    data = request.get_json()
    role.name = data.get("name", role.name)

    if "permissions" in data:
        permissions = Permission.query.filter(Permission.id.in_(data["permissions"])).all()
        role.permissions = permissions

    db.session.commit()
    return jsonify({"message": "Role updated", "role": role.to_dict()}), 200

# Delete a role
@role_bp.route("/delete-role/<int:role_id>", methods=["DELETE"])
def delete_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404

    db.session.delete(role)
    db.session.commit()

    return jsonify({"message": "Role deleted successfully"}), 200

# Assign additional permissions to a role
@role_bp.route("/<int:role_id>/assign_permissions", methods=["POST"])
def assign_permissions(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404

    data = request.get_json()
    permission_ids = data.get("permission_ids", [])

    if not isinstance(permission_ids, list):
        return jsonify({"error": "Invalid permissions format"}), 400

    permissions = Permission.query.filter(Permission.id.in_(permission_ids)).all()

    if not permissions:
        return jsonify({"error": "No valid permissions found"}), 404

    role.permissions.extend(permissions)  
    db.session.commit()

    return jsonify({"message": "Permissions assigned successfully", "role": role.to_dict()}), 200

# Remove a permission from a role
@role_bp.route("/roles/<int:role_id>/remove_permission", methods=["POST"])
def remove_permission(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404

    data = request.get_json()
    permission_id = data.get("permission_id")

    if not permission_id:
        return jsonify({"error": "Permission ID required"}), 400

    permission = Permission.query.get(permission_id)
    if not permission or permission not in role.permissions:
        return jsonify({"error": "Permission not assigned to this role"}), 404

    role.permissions.remove(permission)
    db.session.commit()

    return jsonify({"message": "Permission removed", "role": role.to_dict()}), 200
