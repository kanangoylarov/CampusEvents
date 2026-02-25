from datetime import datetime
from app.extensions import db


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(200))
    room_name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer)
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # One room can host one event at a time
    event = db.relationship('Event', backref='venue', uselist=False, lazy=True)

    def __repr__(self):
        return f'<Room {self.room_name}>'
