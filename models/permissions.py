from models import db

# Association Table for Many-to-Many Relationship (Roles-Permissions)---because many roles can have many permissions and vice versa
# did not make it into a model because there are no extra columns/aspects to add to it
role_permissions = db.Table(
    'role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)
# permissions model
class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False) 
    description = db.Column(db.String(255), nullable=True)
    
    roles = db.relationship("Role", secondary=role_permissions, back_populates="permissions")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
