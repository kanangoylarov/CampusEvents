from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app


def generate_token(user_id):
    payload = {
        'sub': str(user_id),
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(
            hours=current_app.config['JWT_EXPIRATION_HOURS']
        ),
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')


def decode_token(token):
    try:
        payload = jwt.decode(
            token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256']
        )
        return int(payload['sub'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
