from flask import Blueprint, request, jsonify
from models import db
from models.permissions import Permission

permission_bp = Blueprint("permission_bp", __name__)

# Create a new permission
@permission_bp.route("/create-permissions", methods=["POST"])
def create_permission():
    data = request.get_json()
    
    if not data or not data.get("name"):
        return jsonify({"error": "Permission name is required"}), 400

    existing_permission = Permission.query.filter_by(name=data["name"]).first()
    if existing_permission:
        return jsonify({"error": "Permission already exists"}), 409

    new_permission = Permission(name=data["name"], description=data.get("description"))
    db.session.add(new_permission)
    db.session.commit()

    return jsonify({"message": "Permission created successfully", "permission": new_permission.to_dict()}), 201

# Get all permissions
@permission_bp.route("/all-permissions", methods=["GET"])
def get_permissions():
    permissions = Permission.query.all()
    return jsonify([perm.to_dict() for perm in permissions]), 200

# Get a single permission by ID
@permission_bp.route("/permissions/<int:permission_id>", methods=["GET"])
def get_permission(permission_id):
    permission = Permission.query.get(permission_id)
    if not permission:
        return jsonify({"error": "Permission not found"}), 404
    return jsonify(permission.to_dict()), 200

# Update a permission
@permission_bp.route("/permissions/<int:permission_id>", methods=["PUT"])
def update_permission(permission_id):
    permission = Permission.query.get(permission_id)
    if not permission:
        return jsonify({"error": "Permission not found"}), 404

    data = request.get_json()
    permission.name = data.get("name", permission.name)
    permission.description = data.get("description", permission.description)

    db.session.commit()
    return jsonify({"message": "Permission updated", "permission": permission.to_dict()}), 200

# Delete a permission
@permission_bp.route("/delete-permissions/<int:permission_id>", methods=["DELETE"])
def delete_permission(permission_id):
    permission = Permission.query.get(permission_id)
    if not permission:
        return jsonify({"error": "Permission not found"}), 404

    db.session.delete(permission)
    db.session.commit()
    return jsonify({"message": "Permission deleted successfully"}), 200
