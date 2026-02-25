from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extensions import db
from app.models.room_model import Room
from app.utils import cleanup_expired_events, save_uploaded_image, delete_uploaded_image

room_bp = Blueprint('room', __name__)


@room_bp.route('/rooms')
def list_rooms():
    cleanup_expired_events()
    rooms = Room.query.order_by(Room.room_name).all()
    return render_template('rooms/index.html', rooms=rooms)


@room_bp.route('/rooms/create', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        picture_file = request.files.get('picture')
        saved_filename = save_uploaded_image(picture_file)

        new_room = Room(
            room_name=request.form.get('room_name'),
            picture=saved_filename,
            capacity=request.form.get('capacity') or None,
            location=request.form.get('location'),
        )
        db.session.add(new_room)
        db.session.commit()
        flash('Room added successfully!', 'success')
        return redirect(url_for('room.list_rooms'))

    return render_template('rooms/create.html')


@room_bp.route('/rooms/<int:id>/edit', methods=['GET', 'POST'])
def update_room(id):
    room = db.get_or_404(Room, id)

    if request.method == 'POST':
        picture_file = request.files.get('picture')
        saved_filename = save_uploaded_image(picture_file)
        if saved_filename:
            delete_uploaded_image(room.picture)
            room.picture = saved_filename

        room.room_name = request.form.get('room_name')
        room.location = request.form.get('location')
        room.capacity = request.form.get('capacity') or None
        db.session.commit()
        flash('Room updated successfully!', 'success')
        return redirect(url_for('room.list_rooms'))

    return render_template('rooms/edit.html', room=room)


@room_bp.route('/rooms/<int:id>/delete', methods=['POST'])
def delete_room(id):
    room = db.get_or_404(Room, id)
    delete_uploaded_image(room.picture)
    db.session.delete(room)
    db.session.commit()
    flash('Room deleted successfully!', 'success')
    return redirect(url_for('room.list_rooms'))
