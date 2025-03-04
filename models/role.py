from models import db
from models.permissions import role_permissions  
from sqlalchemy.orm import relationship


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Many-to-Many relationship with permissions
    permissions = db.relationship("Permission", secondary=role_permissions, back_populates="roles")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "permissions": [perm.to_dict() for perm in self.permissions]
        }
    user = relationship("User", back_populates="role") 