from app.extensions import db
from app.models.user_model import User


def find_by_email(email):
    return User.query.filter_by(email=email).first()


def get_all():
    return User.query.order_by(User.created_at.desc()).all()


def get_by_id(user_id):
    return db.session.get(User, user_id)


def save(user):
    db.session.add(user)
    db.session.commit()


def update():
    db.session.commit()


def delete(user):
    db.session.delete(user)
    db.session.commit()
