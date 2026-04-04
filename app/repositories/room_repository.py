from app.extensions import db
from app.models.room_model import Room


def get_all_ordered_by_name():
    return Room.query.order_by(Room.room_name).all()


def get_by_id(room_id):
    return db.get_or_404(Room, room_id)


def save(room):
    db.session.add(room)
    db.session.commit()


def update():
    db.session.commit()


def delete(room):
    db.session.delete(room)
    db.session.commit()
