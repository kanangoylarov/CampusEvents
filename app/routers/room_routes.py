from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.services import room_service

room_bp = Blueprint('room', __name__)


@room_bp.route('/rooms')
def list_rooms():
    rooms = room_service.list_rooms()
    return render_template('rooms/index.html', rooms=rooms)


@room_bp.route('/rooms/create')
def create_room_form():
    return render_template('rooms/create.html')


@room_bp.route('/rooms/create', methods=['POST'])
def create_room():
    room_service.create_room(request.form, request.files.get('picture'))
    flash('Room added successfully!', 'success')
    return redirect(url_for('room.list_rooms'))


@room_bp.route('/rooms/<int:id>/edit')
def update_room_form(id):
    room = room_service.get_room(id)
    return render_template('rooms/edit.html', room=room)


@room_bp.route('/rooms/<int:id>/edit', methods=['POST'])
def update_room(id):
    room_service.update_room(id, request.form, request.files.get('picture'))
    flash('Room updated successfully!', 'success')
    return redirect(url_for('room.list_rooms'))


@room_bp.route('/rooms/<int:id>/delete', methods=['POST'])
def delete_room(id):
    room_service.delete_room(id)
    flash('Room deleted successfully!', 'success')
    return redirect(url_for('room.list_rooms'))
