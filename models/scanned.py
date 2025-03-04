from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Scanned(db.Model):
    __tablename__ = 'scanned'  

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), default='pending', nullable=False)
    scanned_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    # Define relationship
    user = db.relationship("User", back_populates="scanned")

    def __repr__(self):  
        return f'<Scanned {self.id}>'
