from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps

from app.services import organization_service
from app.repositories import organization_repository

organization_bp = Blueprint('organization', __name__)


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in first.', 'danger')
            return redirect(url_for('user.login_form'))
        if current_user.role != 'admin':
            flash('You do not have permission to do this.', 'danger')
            return redirect(url_for('organization.list_organizations'))
        return f(*args, **kwargs)
    return decorated


def org_owner_required(f):
    """Allow admin or organization-role user who owns this organization."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in first.', 'danger')
            return redirect(url_for('user.login_form'))
        if current_user.role == 'admin':
            return f(*args, **kwargs)
        org_id = kwargs.get('id')
        if current_user.role == 'organization' and current_user.organization_id and current_user.organization_id == org_id:
            return f(*args, **kwargs)
        flash('You do not have permission to do this.', 'danger')
        return redirect(url_for('organization.list_organizations'))
    return decorated


@organization_bp.get('/organizations')
def list_organizations():
    organizations = organization_service.list_organizations()
    my_org = None
    if current_user.is_authenticated and current_user.role == 'organization' and current_user.organization_id:
        my_org = organization_service.get_organization(current_user.organization_id)
    return render_template('organizations/index.html', organizations=organizations, my_org=my_org)


@organization_bp.get('/organizations/<int:id>')
def view_organization(id):
    org = organization_service.get_organization(id)
    return render_template('organizations/detail.html', org=org)


@organization_bp.get('/organizations/create')
@login_required
def create_organization_form():
    if current_user.role == 'organization' and current_user.organization_id:
        flash('You already have an organization.', 'danger')
        return redirect(url_for('organization.list_organizations'))
    if current_user.role not in ('admin', 'organization'):
        flash('You do not have permission to do this.', 'danger')
        return redirect(url_for('organization.list_organizations'))
    return render_template('organizations/create.html')


@organization_bp.post('/organizations/create')
@login_required
def create_organization():
    if current_user.role == 'organization' and current_user.organization_id:
        flash('You already have an organization.', 'danger')
        return redirect(url_for('organization.list_organizations'))
    if current_user.role not in ('admin', 'organization'):
        flash('You do not have permission to do this.', 'danger')
        return redirect(url_for('organization.list_organizations'))
    org, error = organization_service.create_organization(
        request.form, request.files.get('picture'))
    if error:
        flash(error, 'danger')
        return redirect(url_for('organization.create_organization_form'))
    if current_user.role == 'organization':
        from app.repositories import user_repository
        current_user.organization_id = org.id
        user_repository.update()
    flash('Organization registered successfully!', 'success')
    return redirect(url_for('organization.list_organizations'))


@organization_bp.get('/organizations/<int:id>/edit')
@org_owner_required
def update_organization_form(id):
    org = organization_service.get_organization(id)
    return render_template('organizations/edit.html', org=org)


@organization_bp.post('/organizations/<int:id>/edit')
@org_owner_required
def update_organization(id):
    org, error = organization_service.update_organization(
        id, request.form, request.files.get('picture'))
    if error:
        flash(error, 'danger')
        return redirect(url_for('organization.update_organization_form', id=id))
    flash('Organization updated successfully!', 'success')
    return redirect(url_for('organization.list_organizations'))


@organization_bp.post('/organizations/<int:id>/delete')
@admin_required
def delete_organization(id):
    organization_service.delete_organization(id)
    flash('Organization deleted successfully!', 'success')
    return redirect(url_for('organization.list_organizations'))