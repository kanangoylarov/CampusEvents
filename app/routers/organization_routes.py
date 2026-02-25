from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.services import organization_service

organization_bp = Blueprint('organization', __name__)


@organization_bp.route('/organizations')
def list_organizations():
    organizations = organization_service.list_organizations()
    return render_template('organizations/index.html', organizations=organizations)


@organization_bp.route('/organizations/<int:id>')
def view_organization(id):
    org = organization_service.get_organization(id)
    return render_template('organizations/detail.html', org=org)


@organization_bp.route('/organizations/create')
def create_organization_form():
    return render_template('organizations/create.html')


@organization_bp.route('/organizations/create', methods=['POST'])
def create_organization():
    organization_service.create_organization(request.form, request.files.get('picture'))
    flash('Organization registered successfully!', 'success')
    return redirect(url_for('organization.list_organizations'))


@organization_bp.route('/organizations/<int:id>/edit')
def update_organization_form(id):
    org = organization_service.get_organization(id)
    return render_template('organizations/edit.html', org=org)


@organization_bp.route('/organizations/<int:id>/edit', methods=['POST'])
def update_organization(id):
    organization_service.update_organization(id, request.form, request.files.get('picture'))
    flash('Organization updated successfully!', 'success')
    return redirect(url_for('organization.list_organizations'))


@organization_bp.route('/organizations/<int:id>/delete', methods=['POST'])
def delete_organization(id):
    organization_service.delete_organization(id)
    flash('Organization deleted successfully!', 'success')
    return redirect(url_for('organization.list_organizations'))
