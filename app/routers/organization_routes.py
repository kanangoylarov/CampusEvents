from flask import Blueprint, render_template, request, redirect, url_for, flash
<<<<<<< HEAD
=======
from flask_login import login_required, current_user
from functools import wraps
>>>>>>> origin/kanan

from app.services import organization_service

organization_bp = Blueprint('organization', __name__)


<<<<<<< HEAD
=======
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


>>>>>>> origin/kanan
@organization_bp.get('/organizations')
def list_organizations():
    organizations = organization_service.list_organizations()
    return render_template('organizations/index.html', organizations=organizations)


@organization_bp.get('/organizations/<int:id>')
def view_organization(id):
    org = organization_service.get_organization(id)
    return render_template('organizations/detail.html', org=org)


@organization_bp.get('/organizations/create')
<<<<<<< HEAD
=======
@admin_required
>>>>>>> origin/kanan
def create_organization_form():
    return render_template('organizations/create.html')


@organization_bp.post('/organizations/create')
<<<<<<< HEAD
def create_organization():
    organization_service.create_organization(request.form, request.files.get('picture'))
=======
@admin_required
def create_organization():
    organization_service.create_organization(
        request.form, request.files.get('picture'))
>>>>>>> origin/kanan
    flash('Organization registered successfully!', 'success')
    return redirect(url_for('organization.list_organizations'))


@organization_bp.get('/organizations/<int:id>/edit')
<<<<<<< HEAD
=======
@admin_required
>>>>>>> origin/kanan
def update_organization_form(id):
    org = organization_service.get_organization(id)
    return render_template('organizations/edit.html', org=org)


@organization_bp.post('/organizations/<int:id>/edit')
<<<<<<< HEAD
def update_organization(id):
    organization_service.update_organization(id, request.form, request.files.get('picture'))
=======
@admin_required
def update_organization(id):
    organization_service.update_organization(
        id, request.form, request.files.get('picture'))
>>>>>>> origin/kanan
    flash('Organization updated successfully!', 'success')
    return redirect(url_for('organization.list_organizations'))


@organization_bp.post('/organizations/<int:id>/delete')
<<<<<<< HEAD
def delete_organization(id):
    organization_service.delete_organization(id)
    flash('Organization deleted successfully!', 'success')
    return redirect(url_for('organization.list_organizations'))
=======
@admin_required
def delete_organization(id):
    organization_service.delete_organization(id)
    flash('Organization deleted successfully!', 'success')
    return redirect(url_for('organization.list_organizations'))
>>>>>>> origin/kanan
