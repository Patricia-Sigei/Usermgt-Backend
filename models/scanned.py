from models import db
from .users import User
class Scanned(db.Model):
    __tablename__ = 'scanned'  

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), default='pending', nullable=False)
    scanned_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "status": self.status,
            "scanned_at": self.scanned_at
        }

    
    def __repr__(self):  
        return f'<Scanned {self.id}>'
    # Define relationship--- here to avoid circular imports
    user = db.relationship("User", back_populates="scanned")

