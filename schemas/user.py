# from schemas import ma
# from models.users import User
# from models.role import Role
# from schemas.role import RoleSchema

# class UserSchema(ma.SQLAlchemySchema):
#     class Meta:
#         model = User
#         load_instance = True

#     id = ma.auto_field()
#     name = ma.auto_field()
#     email = ma.auto_field()
#     phone_number = ma.auto_field()
#     role = ma.Nested(RoleSchema, only=["id", "name"])  

# user_schema = UserSchema()
# users_schema = UserSchema(many=True)
