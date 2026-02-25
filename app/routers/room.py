from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extensions import db
from app.models.room_model import Room
from app.utils import cleanup_expired_events

room_bp = Blueprint('room', __name__)


@room_bp.route('/rooms')
def list_rooms():
    cleanup_expired_events()
    rooms = Room.query.order_by(Room.room_name).all()
    return render_template('rooms/index.html', rooms=rooms)


@room_bp.route('/rooms/create', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        new_room = Room(
            room_name=request.form.get('room_name'),
            picture=request.form.get('picture'),
            capacity=request.form.get('capacity') or None,
            location=request.form.get('location'),
        )
        db.session.add(new_room)
        db.session.commit()
        flash('Room added successfully!', 'success')
        return redirect(url_for('room.list_rooms'))

    return render_template('rooms/create.html')
