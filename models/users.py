from models import db
from sqlalchemy import Boolean, ARRAY

class User(db.Model):
    __tablename__ = "user"  

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(Boolean, default=False)
    permissions = db.Column(ARRAY(db.String), default=[])

    # For logging
    def __repr__(self):
        return f"<User {self.name}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "is_admin": self.is_admin,
            "permissions": self.permissions
        }
