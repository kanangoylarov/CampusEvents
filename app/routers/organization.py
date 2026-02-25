from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extensions import db
from app.models.organization_model import Organization
from app.utils import save_uploaded_image, delete_uploaded_image

organization_bp = Blueprint('organization', __name__)


@organization_bp.route('/organizations')
def list_organizations():
    organizations = Organization.query.order_by(Organization.name).all()
    return render_template('organizations/index.html', organizations=organizations)


@organization_bp.route('/organizations/<int:id>')
def view_organization(id):
    org = db.get_or_404(Organization, id)
    return render_template('organizations/detail.html', org=org)


@organization_bp.route('/organizations/create', methods=['GET', 'POST'])
def create_organization():
    if request.method == 'POST':
        picture_file = request.files.get('picture')
        saved_filename = save_uploaded_image(picture_file)

        new_organization = Organization(
            name=request.form.get('name'),
            description=request.form.get('description'),
            picture=saved_filename,
        )
        db.session.add(new_organization)
        db.session.commit()
        flash('Organization registered successfully!', 'success')
        return redirect(url_for('organization.list_organizations'))

    return render_template('organizations/create.html')


@organization_bp.route('/organizations/<int:id>/edit', methods=['GET', 'POST'])
def update_organization(id):
    org = db.get_or_404(Organization, id)

    if request.method == 'POST':
        picture_file = request.files.get('picture')
        saved_filename = save_uploaded_image(picture_file)
        if saved_filename:
            delete_uploaded_image(org.picture)
            org.picture = saved_filename

        org.name = request.form.get('name')
        org.description = request.form.get('description')
        db.session.commit()
        flash('Organization updated successfully!', 'success')
        return redirect(url_for('organization.list_organizations'))

    return render_template('organizations/edit.html', org=org)


@organization_bp.route('/organizations/<int:id>/delete', methods=['POST'])
def delete_organization(id):
    org = db.get_or_404(Organization, id)
    delete_uploaded_image(org.picture)
    db.session.delete(org)
    db.session.commit()
    flash('Organization deleted successfully!', 'success')
    return redirect(url_for('organization.list_organizations'))
