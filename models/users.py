from models import db
import re
from sqlalchemy.orm import validates

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)

    # Relationship with role_id model
    role = db.relationship("Role", back_populates="users")
# regex to validate password
    @validates("password")
    def validate_password(self, key, password):
       
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character.")

        return password  
    # validates the email using regex
    @validates("email")
    def validate_email(self, key, email):
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format. Please enter a valid email address.")
        return email

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "role": self.role.name if self.role else None,
            "scanned": [scanned.to_dict() for scanned in self.scanned] if hasattr(self, "scanned") else [],
            "orders": [order.to_dict() for order in self.orders] if hasattr(self, "orders") else [],
        }
    
    def __repr__(self):
        return f"<User {self.name}>"

# Import Scanned and Orders ..avoids circular imports where they are dependent on each other

from .scanned import Scanned
from .orders import Orders  

# Defining relationships at the bottom to avoid dependencies (circular imports- putting user. makes it recognize that scanned is part of the user relationship)
User.scanned = db.relationship("Scanned", back_populates="user", cascade="all, delete-orphan")
User.orders = db.relationship("Orders", back_populates="user", cascade="all, delete-orphan", lazy=True)
