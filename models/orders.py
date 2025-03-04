from models import db
from .users import User

class Orders(db.Model):
    __tablename__ = 'orders'  

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_name = db.Column(db.String(50), nullable=False)
    order_description = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    space = db.Column(db.String(50), nullable=False)
    vat = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    date_ordered = db.Column(db.Date, nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    dispatch_status = db.Column(db.String(50), nullable=False)
    delivery_charges = db.Column(db.Float, nullable=True)
    reason = db.Column(db.String(50), nullable=True)
    initialiser = db.Column(db.String(50), nullable=True)

    users = db.relationship('User', back_populates='orders')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "order_name": self.order_name,
            "order_description": self.order_description,
            "name": self.name,
            "cost": self.cost,
            "space": self.space,
            "vat": self.vat,
            "quantity": self.quantity,
            "status": self.status,
            "date_ordered": self.date_ordered.isoformat() if self.date_ordered else None,  
            "payment_status": self.payment_status,
            "dispatch_status": self.dispatch_status,
            "delivery_charges": self.delivery_charges,
            "reason": self.reason,
            "initialiser": self.initialiser
        }

    def __repr__(self):
        return f'<Order {self.id}: {self.order_name}>'
