from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from ...models import User

jwt = JWTManager()
bcrypt = Bcrypt()

def create_module(app, **kwargs):
    bcrypt.init_app(app)
    jwt.init_app(app)

    from .controllers import auth_blueprint
    app.register_blueprint(auth_blueprint)

def authenticate(email, password):
    user = get_user_by_email(email)
    
    if not user:
        return None
    
    # Do the passwords match
    if not bcrypt.check_password_hash(user.password, password):
        return None
    
    return user

def get_user_by_email(email) -> User:
    user = User.objects(
        email__exact=email
    ).first()
    
    return user

def encode_password(password: str) -> str:
    return bcrypt.generate_password_hash(str(password))