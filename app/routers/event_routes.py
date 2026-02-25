from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.services import event_service
from app.repositories import organization_repository, room_repository, event_repository

event_bp = Blueprint('event', __name__)


@event_bp.get('/events')
def list_events():
    raw_filters = {
        'org_id': request.args.get('org_id', ''),
        'date_from': request.args.get('date_from', ''),
        'date_to': request.args.get('date_to', ''),
        'time_from': request.args.get('time_from', ''),
        'time_to': request.args.get('time_to', ''),
    }
    events = event_service.list_events(raw_filters)
    organizations = organization_repository.get_all_ordered_by_name()
    active_filters = any(v.strip() for v in raw_filters.values())
    return render_template(
        'events/index.html',
        events=events,
        organizations=organizations,
        filters=raw_filters,
        active_filters=active_filters,
    )


@event_bp.get('/events/create')
def create_event_form():
    organizations = organization_repository.get_all_ordered_by_name()
    rooms = room_repository.get_all_ordered_by_name()
    return render_template('events/create.html', organizations=organizations, rooms=rooms)


@event_bp.post('/events/create')
def create_event():
    event, error = event_service.create_event(request.form, request.files.get('picture'))
    if error:
        flash(error)
        organizations = organization_repository.get_all_ordered_by_name()
        rooms = room_repository.get_all_ordered_by_name()
        return render_template('events/create.html',
                               organizations=organizations, rooms=rooms)
    flash('Event created successfully!', 'success')
    return redirect(url_for('event.list_events'))


@event_bp.get('/events/<int:id>/edit')
def update_event_form(id):
    event = event_repository.get_by_id(id)
    organizations = organization_repository.get_all_ordered_by_name()
    rooms = room_repository.get_all_ordered_by_name()
    return render_template('events/edit.html', event=event,
                           organizations=organizations, rooms=rooms)


@event_bp.post('/events/<int:id>/edit')
def update_event(id):
    event, error = event_service.update_event(id, request.form, request.files.get('picture'))
    if error:
        flash(error)
        organizations = organization_repository.get_all_ordered_by_name()
        rooms = room_repository.get_all_ordered_by_name()
        return render_template('events/edit.html', event=event,
                               organizations=organizations, rooms=rooms)
    flash('Event updated successfully!', 'success')
    return redirect(url_for('event.list_events'))


@event_bp.post('/events/<int:id>/delete')
def delete_event(id):
    event_service.delete_event(id)
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('event.list_events'))
