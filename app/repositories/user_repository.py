from app.extensions import db
from app.models.user_model import User


def find_by_email(email):
    return User.query.filter_by(email=email).first()


def save(user):
    db.session.add(user)
    db.session.commit()
