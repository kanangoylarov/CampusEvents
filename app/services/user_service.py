from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from app.models.user_model import User
from app.repositories import user_repository


def register_user(full_name, email, password, role='user'):
    if user_repository.find_by_email(email):
        return None, None, 'An account with this email already exists.'
    user = User(
        full_name=full_name,
        email=email,
        password=generate_password_hash(password),
        role=role,
    )
    user_repository.save(user)
    # Generate JWT token upon successful registration
    access_token = create_access_token(identity=user.id)
    return user, access_token, None


def authenticate(email, password):
    user = user_repository.find_by_email(email)
    if user and check_password_hash(user.password, password):
        # Generate JWT token upon successful authentication
        access_token = create_access_token(identity=user.id)
        return user, access_token
    return None, None
