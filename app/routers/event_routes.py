from flask import Blueprint, render_template, request, redirect, url_for, flash
<<<<<<< HEAD
=======
from flask_login import login_required, current_user
>>>>>>> origin/kanan

from app.services import event_service
from app.repositories import organization_repository, room_repository, event_repository

<<<<<<< HEAD
=======

def _check_org_ownership(event):
    """Return True if current user is organization and does NOT own this event."""
    if current_user.role != 'organization':
        return False
    if not event:
        flash('Event not found.', 'danger')
        return True
    user_org = current_user.organization_id
    event_org = event.organization_id
    # both must exist and match (cast to int to avoid str/int mismatch)
    if user_org and event_org and int(user_org) == int(event_org):
        return False
    flash('You can only modify your own organization\'s events.', 'danger')
    return True

>>>>>>> origin/kanan
event_bp = Blueprint('event', __name__)


@event_bp.get('/events')
def list_events():
    raw_filters = {
<<<<<<< HEAD
        'org_id': request.args.get('org_id', ''),
        'date_from': request.args.get('date_from', ''),
        'date_to': request.args.get('date_to', ''),
        'time_from': request.args.get('time_from', ''),
        'time_to': request.args.get('time_to', ''),
=======
        'org_id':      request.args.get('org_id', ''),
        'date_from':   request.args.get('date_from', ''),
        'date_to':     request.args.get('date_to', ''),
        'time_from':   request.args.get('time_from', ''),
        'time_to':     request.args.get('time_to', ''),
>>>>>>> origin/kanan
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


<<<<<<< HEAD
=======
# ── admin + organization (RBAC in __init__.py) ───────────
>>>>>>> origin/kanan
@event_bp.get('/events/create')
def create_event_form():
    organizations = organization_repository.get_all_ordered_by_name()
    rooms = room_repository.get_all_ordered_by_name()
<<<<<<< HEAD
    return render_template('events/create.html', organizations=organizations, rooms=rooms)
=======
    return render_template('events/create.html',
                           organizations=organizations, rooms=rooms)
>>>>>>> origin/kanan


@event_bp.post('/events/create')
def create_event():
<<<<<<< HEAD
    event, error = event_service.create_event(request.form, request.files.get('picture'))
    if error:
        flash(error)
=======
    form_data = request.form.to_dict()
    if current_user.role == 'organization' and current_user.organization_id:
        form_data['organization_id'] = str(current_user.organization_id)
    event, error = event_service.create_event(
        form_data, request.files.get('picture'))
    if error:
        flash(error, 'danger')
>>>>>>> origin/kanan
        organizations = organization_repository.get_all_ordered_by_name()
        rooms = room_repository.get_all_ordered_by_name()
        return render_template('events/create.html',
                               organizations=organizations, rooms=rooms)
    flash('Event created successfully!', 'success')
    return redirect(url_for('event.list_events'))


@event_bp.get('/events/<int:id>/edit')
def update_event_form(id):
    event = event_repository.get_by_id(id)
<<<<<<< HEAD
=======
    if _check_org_ownership(event):
        return redirect(url_for('event.list_events'))
>>>>>>> origin/kanan
    organizations = organization_repository.get_all_ordered_by_name()
    rooms = room_repository.get_all_ordered_by_name()
    return render_template('events/edit.html', event=event,
                           organizations=organizations, rooms=rooms)


@event_bp.post('/events/<int:id>/edit')
def update_event(id):
<<<<<<< HEAD
    event, error = event_service.update_event(id, request.form, request.files.get('picture'))
    if error:
        flash(error)
=======
    event = event_repository.get_by_id(id)
    if _check_org_ownership(event):
        return redirect(url_for('event.list_events'))
    form_data = request.form.to_dict()
    if current_user.role == 'organization' and current_user.organization_id:
        form_data['organization_id'] = str(current_user.organization_id)
    event, error = event_service.update_event(
        id, form_data, request.files.get('picture'))
    if error:
        flash(error, 'danger')
>>>>>>> origin/kanan
        organizations = organization_repository.get_all_ordered_by_name()
        rooms = room_repository.get_all_ordered_by_name()
        return render_template('events/edit.html', event=event,
                               organizations=organizations, rooms=rooms)
    flash('Event updated successfully!', 'success')
    return redirect(url_for('event.list_events'))


@event_bp.post('/events/<int:id>/delete')
def delete_event(id):
<<<<<<< HEAD
    event_service.delete_event(id)
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('event.list_events'))
=======
    event = event_repository.get_by_id(id)
    if _check_org_ownership(event):
        return redirect(url_for('event.list_events'))
    event_service.delete_event(id)
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('event.list_events'))


# ── Yalnız login olmuş user ───────────────────────────────
@event_bp.post('/events/<int:id>/register')
@login_required
def register_event(id):
    event = event_repository.get_by_id(id)
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('event.list_events'))
    flash(f'Successfully registered for "{event.name}"!', 'success')
    return redirect(url_for('event.list_events'))
>>>>>>> origin/kanan
