from app import ma
from app.models.user import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User  
        load_instance = True  

    id = ma.auto_field()  
    username = ma.auto_field()  
    password = ma.auto_field()  

