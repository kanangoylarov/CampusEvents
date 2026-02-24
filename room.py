from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from db import Room, db

room_bp = Blueprint('room', __name__)
@room_bp.route('/rooms')
def list_rooms():
    rooms = Room.query.all()
    return render_template('rooms.html', rooms=rooms)

@room_bp.route('/rooms/create', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        room_name = request.form.get('room_name')
        picture = request.form.get('picture')
        capacity = request.form.get('capacity')
        location = request.form.get('location')

        new_room = Room(
            room_name=room_name,
            picture=picture,
            capacity=capacity,
            location=location
        )
        db.session.add(new_room)
        db.session.commit()

        flash('Room created successfully!', 'success')
        return redirect(url_for('room.list_rooms'))
    return render_template('create_room.html')  
