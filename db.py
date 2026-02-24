from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(200))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    private = db.Column(db.Boolean, default=False)
    eligible_rooms = db.Column(db.String(200))
    organization_id = db.Column(db.Integer)
    date = db.Column(db.Date)
    for_registration = db.Column(db.String(200))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    room_id = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

def new_func(db):
    class Organization(db.Model):
        __tablename__ = 'organizations'
        id = db.Column(db.Integer, primary_key=True)
        picture = db.Column(db.String(200))
        name = db.Column(db.String(100), nullable=False)
        events_id = db.Column(db.String(200))
        description = db.Column(db.Text)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

new_func(db)

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(200))
    room_name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer)
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

