# User Management Microservice
This microservice is a core component of an Inventory Management System, handling user authentication, role-based access control, and account management.

## Features
- User Registration (Admin only)
- User Authentication (JWT)
- Retrieve User Information
- Update User Profile
- Delete Users (Admin only)
- Role-based Access Control (Admins & Regular Users)
## Technologies Used
- Flask (Web framework)
- Flask-JWT-Extended (JWT authentication)
- Flask-Bcrypt (Password hashing)
- PostgreSQL (Database)
- SQLAlchemy (ORM)

## Installation

1. Clone the repository

    git clone https://github.com/Patricia-Sigei/Usermgt-Backend 

    cd Usermgt-Backend

2. Create and activate a virtual environment
s
    pipenv shell


3. Install dependencies

    pipenv install 

4. Set up environment variables

Create a .env file and add:

    SECRET_KEY=your_secret_key 

    DATABASE_URL=postgresql://username:password@localhost/db_name

    JWT_SECRET_KEY=your_jwt_secret_key

5. Run database migrations

    flask db init
    
    flask db migrate -m "Initial Migration"

    flask db upgrade

6. Start the server

    flask run or python app.py

## License
This project is open-source and licensed under the MIT License.