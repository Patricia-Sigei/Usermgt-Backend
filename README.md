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

    git clone https://github.com/Patricia-Sigei/inventory-management-user-service.git
    cd inventory-management-user-service

2. Create and activate a virtual environment
s
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies

    pip install -r requirements.txt

4. Set up environment variables

Create a .env file and add:

    SECRET_KEY=your_secret_key
    DATABASE_URL=postgresql://username:password@localhost/db_name
    JWT_SECRET_KEY=your_jwt_secret_key

5. Run database migrations

    flask db upgrade

6. Start the server

 flask run or python app.py

## API Endpoints
- Authentication

    Method	    Endpoint	                    Description
    POST	  /auth/login	                 User login (returns JWT token)
    POST      /auth/reset-password           User Password Reset

- User Management

    Method	       Endpoint	                        Description	                     Access
    POST	     /users/create	                   Create a new user	              Admin
    GET	         /users/all	                       Get all users	                  Admin
    GET	         /users/<user_id>	               Get user by ID	                  User/Admin
    PUT	         /users/<user_id>	               Update user by ID	              User/Admin
    DELETE	     /users/<user_id>	               Delete user by ID	              Admin

## Part of the Inventory Management System
This microservice is responsible for managing user accounts and access control within a larger Inventory Management System. It ensures that:

- Only authorized users can access inventory-related resources.
- Admins can create and manage users.
- Users can only access their own profiles.

This service works alongside other microservices such as:

- Fixed assets Service (Handles stock and product tracking)
- Order Service (Manages customer orders)
- Vendor Service (Connects with assets vendors)

## Authentication & Authorization
- JWT tokens are required for all routes (except login).
- Users can only access their own profile.
- Admins (role_id = 1) can create, view, update, and delete users.
## License
This project is open-source and licensed under the MIT License.