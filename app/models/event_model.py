from datetime import datetime
from app.extensions import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(200))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    private = db.Column(db.Boolean, default=False)
    date = db.Column(db.Date)
    for_registration = db.Column(db.String(200))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    capacity = db.Column(db.Integer)

    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Event {self.name}>'
