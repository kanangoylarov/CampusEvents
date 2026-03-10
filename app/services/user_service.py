from werkzeug.security import generate_password_hash, check_password_hash
<<<<<<< HEAD
from flask_jwt_extended import create_access_token
=======
>>>>>>> origin/kanan

from app.models.user_model import User
from app.repositories import user_repository


<<<<<<< HEAD
def register_user(full_name, email, password, role='user'):
    if user_repository.find_by_email(email):
        return None, None, 'An account with this email already exists.'
=======
def register_user(full_name, email, password, role='user', organization_id=None):
    if user_repository.find_by_email(email):
        return None, 'An account with this email already exists.'
>>>>>>> origin/kanan
    user = User(
        full_name=full_name,
        email=email,
        password=generate_password_hash(password),
        role=role,
<<<<<<< HEAD
    )
    user_repository.save(user)
    # Generate JWT token upon successful registration
    access_token = create_access_token(identity=user.id)
    return user, access_token, None
=======
        organization_id=organization_id if role == 'organization' else None,
    )
    user_repository.save(user)
    return user, None
>>>>>>> origin/kanan


def authenticate(email, password):
    user = user_repository.find_by_email(email)
    if user and check_password_hash(user.password, password):
<<<<<<< HEAD
        # Generate JWT token upon successful authentication
        access_token = create_access_token(identity=user.id)
        return user, access_token
    return None, None
=======
        return user
    return None


def list_users():
    return user_repository.get_all()


def get_user(user_id):
    return user_repository.get_by_id(user_id)


def update_user(user_id, full_name, email, role, password=None, organization_id=None):
    user = user_repository.get_by_id(user_id)
    if not user:
        return None, 'User not found.'
    existing = user_repository.find_by_email(email)
    if existing and existing.id != user.id:
        return None, 'An account with this email already exists.'
    user.full_name = full_name
    user.email = email
    user.role = role
    user.organization_id = organization_id if role == 'organization' else None
    if password:
        user.password = generate_password_hash(password)
    user_repository.update()
    return user, None


def delete_user(user_id):
    user = user_repository.get_by_id(user_id)
    if user:
        user_repository.delete(user)
>>>>>>> origin/kanan
