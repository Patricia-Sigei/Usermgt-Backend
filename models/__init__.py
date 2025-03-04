from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models 
from .role import Role
from .permissions import Permission
from .users import User
from .orders import Orders
from .scanned import Scanned
