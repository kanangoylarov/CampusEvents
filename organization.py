from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from db import db, Organization

organization_bp = Blueprint('organization', __name__)
@organization_bp.route('/organizations')
def list_organizations():
    organizations = Organization.query.all()
    return render_template('organizations.html', organizations=organizations)

@organization_bp.route('/organizations/create', methods=['GET', 'POST'])
def create_organization():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        picture = request.form.get('picture')

        new_organization = Organization(
            name=name,
            description=description,
            picture=picture
        )
        db.session.add(new_organization)
        db.session.commit()

        flash('Organization created successfully!', 'success')
        return redirect(url_for('organization.list_organizations'))
    return render_template('create_organization.html')