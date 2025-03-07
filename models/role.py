from models import db
from .permissions import role_permissions  
from sqlalchemy.orm import relationship

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Many-to-Many relationship with permissions
    permissions = db.relationship("Permission", secondary=role_permissions, back_populates="roles")
    users = relationship("User", back_populates="role") 

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "permissions": [perm.to_dict() for perm in self.permissions],
            "users": [user.to_dict() for user in self.users] 
            
        }
   