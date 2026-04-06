from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.services import room_service

room_bp = Blueprint('room', __name__)


@room_bp.get('/rooms')
@login_required
def list_rooms():
    if current_user.role not in ('admin', 'organization'):
        flash('You do not have permission to view this page.', 'danger')
        return redirect(url_for('main.index'))
    rooms = room_service.list_rooms()
    return render_template('rooms/index.html', rooms=rooms)


@room_bp.get('/rooms/create')
@login_required
def create_room_form():
    if current_user.role != 'admin':
        flash('You do not have permission to do this.', 'danger')
        return redirect(url_for('room.list_rooms'))
    return render_template('rooms/create.html')


@room_bp.post('/rooms/create')
@login_required
def create_room():
    if current_user.role != 'admin':
        flash('You do not have permission to do this.', 'danger')
        return redirect(url_for('room.list_rooms'))
    room_service.create_room(request.form, request.files.get('picture'))
    flash('Room added successfully!', 'success')
    return redirect(url_for('room.list_rooms'))


@room_bp.get('/rooms/<int:id>/edit')
@login_required
def update_room_form(id):
    if current_user.role != 'admin':
        flash('You do not have permission to do this.', 'danger')
        return redirect(url_for('room.list_rooms'))
    room = room_service.get_room(id)
    return render_template('rooms/edit.html', room=room)


@room_bp.post('/rooms/<int:id>/edit')
@login_required
def update_room(id):
    if current_user.role != 'admin':
        flash('You do not have permission to do this.', 'danger')
        return redirect(url_for('room.list_rooms'))
    room_service.update_room(id, request.form, request.files.get('picture'))
    flash('Room updated successfully!', 'success')
    return redirect(url_for('room.list_rooms'))


@room_bp.post('/rooms/<int:id>/delete')
@login_required
def delete_room(id):
    if current_user.role != 'admin':
        flash('You do not have permission to do this.', 'danger')
        return redirect(url_for('room.list_rooms'))
    room_service.delete_room(id)
    flash('Room deleted successfully!', 'success')
    return redirect(url_for('room.list_rooms'))
