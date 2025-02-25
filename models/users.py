from models import db
from sqlalchemy.orm import relationship

# match the tables creates using postgres sql (hybrid stuff)
class User(db.Model):
    __tablename__ = "user"  

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # Relationships
    permissions = relationship("UserPermission", back_populates="user")
# for logging
    def __repr__(self):
        return f"<User {self.name}>"
