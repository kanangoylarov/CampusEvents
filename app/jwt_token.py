from app.jwt_utils import generate_token


def create_user_token(user_id):
    return generate_token(user_id)

