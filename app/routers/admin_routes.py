from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user

from app.services import user_service, event_service, organization_service, room_service
from app.repositories import (
    user_repository, event_repository,
    organization_repository, room_repository,
)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.before_request
def check_admin():
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('user.login_form'))


@admin_bp.get('/')
def dashboard():
    all_users = user_repository.get_all()
    stats = {
        'users': len(all_users),
        'events': len(event_repository.get_all()),
        'organizations': len(organization_repository.get_all_ordered_by_name()),
        'rooms': len(room_repository.get_all_ordered_by_name()),
    }
    recent_users = all_users[:5]
    return render_template('admin/dashboard.html', stats=stats, recent_users=recent_users)


@admin_bp.get('/users')
def list_users():
    users = user_service.list_users()
    return render_template('admin/users/index.html', users=users)


@admin_bp.get('/users/create')
def create_user_form():
    organizations = organization_repository.get_all_ordered_by_name()
    return render_template('admin/users/create.html', organizations=organizations)


@admin_bp.post('/users/create')
def create_user():
    user, error = user_service.register_user(
        full_name=request.form.get('full_name'),
        email=request.form.get('email'),
        password=request.form.get('password'),
        role=request.form.get('role', 'user'),
        organization_id=request.form.get('organization_id') or None,
    )
    if error:
        flash(error, 'danger')
        return redirect(url_for('admin.create_user_form'))
    flash('User created successfully!', 'success')
    return redirect(url_for('admin.list_users'))


@admin_bp.get('/users/<int:id>/edit')
def edit_user_form(id):
    user = user_service.get_user(id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin.list_users'))
    organizations = organization_repository.get_all_ordered_by_name()
    return render_template('admin/users/edit.html', user=user, organizations=organizations)


@admin_bp.post('/users/<int:id>/edit')
def edit_user(id):
    user, error = user_service.update_user(
        user_id=id,
        full_name=request.form.get('full_name'),
        email=request.form.get('email'),
        role=request.form.get('role', 'user'),
        password=request.form.get('password') or None,
        organization_id=request.form.get('organization_id') or None,
    )
    if error:
        flash(error, 'danger')
        return redirect(url_for('admin.edit_user_form', id=id))
    flash('User updated successfully!', 'success')
    return redirect(url_for('admin.list_users'))


@admin_bp.post('/users/<int:id>/delete')
def delete_user(id):
    if current_user.id == id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.list_users'))
    user_service.delete_user(id)
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.list_users'))


@admin_bp.post('/users/<int:id>/set-role')
def set_user_role(id):
    if current_user.id == id:
        flash('You cannot change your own role.', 'danger')
        return redirect(url_for('admin.list_users'))
    role = request.form.get('role')
    if role not in ('user', 'organization', 'admin'):
        flash('Invalid role.', 'danger')
        return redirect(url_for('admin.list_users'))
    target = user_service.get_user(id)
    if not target:
        flash('User not found.', 'danger')
        return redirect(url_for('admin.list_users'))
    organization_id = request.form.get('organization_id') or target.organization_id
    user_service.update_user(
        user_id=id,
        full_name=target.full_name,
        email=target.email,
        role=role,
        password=None,
        organization_id=organization_id,
    )
    flash(f'Permission updated — {target.full_name} is now "{role}".', 'success')
    return redirect(url_for('admin.list_users'))


@admin_bp.get('/events')
def list_events():
    events = event_repository.get_all()
    return render_template('admin/events/index.html', events=events)


@admin_bp.get('/events/create')
def create_event_form():
    organizations = organization_repository.get_all_ordered_by_name()
    rooms = room_repository.get_all_ordered_by_name()
    return render_template('admin/events/create.html',
                           organizations=organizations, rooms=rooms)


@admin_bp.post('/events/create')
def create_event():
    event, error = event_service.create_event(
        request.form, request.files.get('picture'))
    if error:
        flash(error, 'danger')
        return redirect(url_for('admin.create_event_form'))
    flash('Event created successfully!', 'success')
    return redirect(url_for('admin.list_events'))


@admin_bp.get('/events/<int:id>/edit')
def edit_event_form(id):
    event = event_repository.get_by_id(id)
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('admin.list_events'))
    organizations = organization_repository.get_all_ordered_by_name()
    rooms = room_repository.get_all_ordered_by_name()
    return render_template('admin/events/edit.html', event=event,
                           organizations=organizations, rooms=rooms)


@admin_bp.post('/events/<int:id>/edit')
def edit_event(id):
    event, error = event_service.update_event(
        id, request.form, request.files.get('picture'))
    if error:
        flash(error, 'danger')
        return redirect(url_for('admin.edit_event_form', id=id))
    flash('Event updated successfully!', 'success')
    return redirect(url_for('admin.list_events'))


@admin_bp.post('/events/<int:id>/delete')
def delete_event(id):
    event_service.delete_event(id)
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('admin.list_events'))


@admin_bp.get('/organizations')
def list_organizations():
    organizations = organization_service.list_organizations()
    return render_template('admin/organizations/index.html',
                           organizations=organizations)


@admin_bp.get('/organizations/create')
def create_organization_form():
    return render_template('admin/organizations/create.html')


@admin_bp.post('/organizations/create')
def create_organization():
    org, error = organization_service.create_organization(
        request.form, request.files.get('picture'))
    if error:
        flash(error, 'danger')
        return redirect(url_for('admin.create_organization_form'))
    flash('Organization created successfully!', 'success')
    return redirect(url_for('admin.list_organizations'))


@admin_bp.get('/organizations/<int:id>/edit')
def edit_organization_form(id):
    org = organization_service.get_organization(id)
    if not org:
        flash('Organization not found.', 'danger')
        return redirect(url_for('admin.list_organizations'))
    return render_template('admin/organizations/edit.html', organization=org)


@admin_bp.post('/organizations/<int:id>/edit')
def edit_organization(id):
    org, error = organization_service.update_organization(
        id, request.form, request.files.get('picture'))
    if error:
        flash(error, 'danger')
        return redirect(url_for('admin.edit_organization_form', id=id))
    flash('Organization updated successfully!', 'success')
    return redirect(url_for('admin.list_organizations'))


@admin_bp.post('/organizations/<int:id>/delete')
def delete_organization(id):
    organization_service.delete_organization(id)
    flash('Organization deleted successfully!', 'success')
    return redirect(url_for('admin.list_organizations'))


@admin_bp.get('/rooms')
def list_rooms():
    rooms = room_service.list_rooms()
    return render_template('admin/rooms/index.html', rooms=rooms)


@admin_bp.get('/rooms/create')
def create_room_form():
    return render_template('admin/rooms/create.html')


@admin_bp.post('/rooms/create')
def create_room():
    room, error = room_service.create_room(
        request.form, request.files.get('picture'))
    if error:
        flash(error, 'danger')
        return redirect(url_for('admin.create_room_form'))
    flash('Room created successfully!', 'success')
    return redirect(url_for('admin.list_rooms'))


@admin_bp.get('/rooms/<int:id>/edit')
def edit_room_form(id):
    room = room_service.get_room(id)
    if not room:
        flash('Room not found.', 'danger')
        return redirect(url_for('admin.list_rooms'))
    return render_template('admin/rooms/edit.html', room=room)


@admin_bp.post('/rooms/<int:id>/edit')
def edit_room(id):
    room, error = room_service.update_room(
        id, request.form, request.files.get('picture'))
    if error:
        flash(error, 'danger')
        return redirect(url_for('admin.edit_room_form', id=id))
    flash('Room updated successfully!', 'success')
    return redirect(url_for('admin.list_rooms'))


@admin_bp.post('/rooms/<int:id>/delete')
def delete_room(id):
    room_service.delete_room(id)
    flash('Room deleted successfully!', 'success')
    return redirect(url_for('admin.list_rooms'))
