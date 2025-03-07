from models import db
from .users import User

class Request(db.Model):
    __tablename__ = "request"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    status = db.Column(db.String(50), default='pending')
    requested_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    asset_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    asset_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "requested_at": self.requested_at,
            "asset_id": self.asset_id,
            "user_name": self.user_name,
            "asset_name": self.asset_name,
            "user_id": self.user_id
        }

    
    def __repr__(self):  
        return f'<Scanned {self.id}>'
    # Define relationship--- here to avoid circular imports--- the class will be already loaded before defining the relationship
    user = db.relationship("User", back_populates="requests")