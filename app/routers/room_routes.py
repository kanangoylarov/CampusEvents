from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from functools import wraps

from app.services import room_service

room_bp = Blueprint('room', __name__)


def _admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in first.', 'danger')
            return redirect(url_for('user.login_form'))
        if current_user.role != 'admin':
            flash('You do not have permission to do this.', 'danger')
            return redirect(url_for('room.list_rooms'))
        return f(*args, **kwargs)
    return decorated


@room_bp.get('/rooms')
def list_rooms():
    rooms = room_service.list_rooms()
    return render_template('rooms/index.html', rooms=rooms)


@room_bp.get('/rooms/create')
@_admin_required
def create_room_form():
    return render_template('rooms/create.html')


@room_bp.post('/rooms/create')
@_admin_required
def create_room():
    room, error = room_service.create_room(request.form, request.files.get('picture'))
    if error:
        flash(error, 'danger')
        return redirect(url_for('room.create_room_form'))
    flash('Room added successfully!', 'success')
    return redirect(url_for('room.list_rooms'))


@room_bp.get('/rooms/<int:id>/edit')
@_admin_required
def update_room_form(id):
    room = room_service.get_room(id)
    return render_template('rooms/edit.html', room=room)


@room_bp.post('/rooms/<int:id>/edit')
@_admin_required
def update_room(id):
    room, error = room_service.update_room(id, request.form, request.files.get('picture'))
    if error:
        flash(error, 'danger')
        return redirect(url_for('room.update_room_form', id=id))
    flash('Room updated successfully!', 'success')
    return redirect(url_for('room.list_rooms'))


@room_bp.post('/rooms/<int:id>/delete')
@_admin_required
def delete_room(id):
    room_service.delete_room(id)
    flash('Room deleted successfully!', 'success')
    return redirect(url_for('room.list_rooms'))
