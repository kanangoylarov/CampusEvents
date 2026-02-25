from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extensions import db
from app.models.organization_model import Organization

organization_bp = Blueprint('organization', __name__)


@organization_bp.route('/organizations')
def list_organizations():
    organizations = Organization.query.order_by(Organization.name).all()
    return render_template('organizations/index.html', organizations=organizations)


@organization_bp.route('/organizations/create', methods=['GET', 'POST'])
def create_organization():
    if request.method == 'POST':
        new_organization = Organization(
            name=request.form.get('name'),
            description=request.form.get('description'),
            picture=request.form.get('picture'),
        )
        db.session.add(new_organization)
        db.session.commit()
        flash('Organization registered successfully!', 'success')
        return redirect(url_for('organization.list_organizations'))

    return render_template('organizations/create.html')
