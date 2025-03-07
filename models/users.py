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
    requests = db.relationship("Request", back_populates="user", cascade="all, delete-orphan")
    orders = db.relationship("Orders", back_populates="user", cascade="all, delete-orphan")
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
    
     # Validate phone number with regex
    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        phone_regex = r"^\d{10}$"  
        if not re.match(phone_regex, phone_number):
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone_number

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "role": self.role.name if self.role else None,
            "requests": [request.to_dict() for request in self.requests] if self.requests else [],           
            "orders": [order.to_dict() for order in self.orders] if hasattr(self, "orders") else []
        }
    
    def __repr__(self):
        return f"<User {self.name}>"

# Import requests and Orders ..avoids circular imports where they are dependent on each other

from .requests import  Request
from .orders import Orders  

# Defining relationships at the bottom to avoid dependencies (circular imports- putting user. makes it recognize that requests and orders are part of the user relationship)

