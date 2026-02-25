from werkzeug.security import generate_password_hash, check_password_hash

from app.models.user_model import User
from app.repositories import user_repository


def register_user(full_name, email, password, role='user'):
    if user_repository.find_by_email(email):
        return None, 'An account with this email already exists.'
    user = User(
        full_name=full_name,
        email=email,
        password=generate_password_hash(password),
        role=role,
    )
    user_repository.save(user)
    return user, None


def authenticate(email, password):
    user = user_repository.find_by_email(email)
    if user and check_password_hash(user.password, password):
        return user
    return None
