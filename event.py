from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import Event, db

event_bp = Blueprint('event', __name__)

@event_bp.route('/events')
def list_events():
    events = Event.query.all()
    return render_template('events.html', events=events)

@event_bp.route('/events/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        picture = request.form.get('picture')
        private = request.form.get('private') == 'off'
        eligible_rooms = request.form.get('eligible_rooms')
        organization_id = request.form.get('organization_id')
        date = request.form.get('date')
        for_registration = request.form.get('for_registration')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        room_id = request.form.get('room_id')
        capacity = request.form.get('capacity')

        new_event = Event(
            name=name,
            description=description,
            picture=picture,
            private=private,
            eligible_rooms=eligible_rooms,
            organization_id=organization_id,
            date=date,
            for_registration=for_registration,
            start_time=start_time,
            end_time=end_time,
            room_id=room_id,
            capacity=capacity
        )
        db.session.add(new_event)
        db.session.commit()

        flash('Event created successfully!', 'success')
        return redirect(url_for('event.list_events'))
    return render_template('create_event.html')


