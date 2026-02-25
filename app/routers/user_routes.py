from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from app.services import user_service

user_bp = Blueprint('user', __name__)


@user_bp.route('/register')
def register_form():
    return render_template('user/register.html')


@user_bp.route('/register', methods=['POST'])
def register():
    user, error = user_service.register_user(
        full_name=request.form.get('full_name'),
        email=request.form.get('email'),
        password=request.form.get('password'),
        role=request.form.get('role', 'user'),
    )
    if error:
        flash(error)
        return redirect(url_for('user.register_form'))
    flash('Account created successfully! Please log in.', 'success')
    return redirect(url_for('user.login_form'))


@user_bp.route('/login')
def login_form():
    return render_template('user/login.html')


@user_bp.route('/login', methods=['POST'])
def login():
    user = user_service.authenticate(
        email=request.form.get('email'),
        password=request.form.get('password'),
    )
    if user:
        login_user(user)
        flash(f'Welcome back, {user.full_name}!', 'success')
        return redirect(url_for('main.index'))
    flash('Invalid email or password.')
    return redirect(url_for('user.login_form'))


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('user.login_form'))
