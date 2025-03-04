from models import db
from .role import Role  
from .scanned import Scanned
from.orders import Orders

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)

    # Relationships
    role = db.relationship("Role", back_populates="users")
    scanned = db.relationship("Scanned", back_populates="user", cascade="all, delete-orphan", lazy=True)  
    orders = db.relationship("Orders", back_populates="user", cascade="all, delete-orphan", lazy=True)  

    def __repr__(self):
        return f"<User {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "role": self.role.name if self.role else None,
            "scanned": [scanned.to_dict() for scanned in self.scanned],  
            "orders": [order.to_dict() for order in self.orders]  
        }
