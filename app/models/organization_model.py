from datetime import datetime
from app.extensions import db


class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(200))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # One organization can host many events
    events = db.relationship('Event', backref='organizer', lazy=True)

    def __repr__(self):
        return f'<Organization {self.name}>'
