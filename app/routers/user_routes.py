from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, current_app
from flask_login import login_user, logout_user, login_required, current_user

from app.services import user_service
from app.jwt_utils import generate_token

user_bp = Blueprint('user', __name__)


@user_bp.get('/register')
def register_form():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('user/register.html')


@user_bp.post('/register')
def register():
    full_name = (request.form.get('full_name') or '').strip()
    email = (request.form.get('email') or '').strip()
    password = request.form.get('password') or ''
    if not full_name or not email or not password:
        flash('All fields are required.', 'danger')
        return redirect(url_for('user.register_form'))
    if len(password) < 6:
        flash('Password must be at least 6 characters.', 'danger')
        return redirect(url_for('user.register_form'))
    user, error = user_service.register_user(
        full_name=full_name,
        email=email,
        password=password,
        role='user',
    )
    if error:
        flash(error, 'danger')
        return redirect(url_for('user.register_form'))
    flash('Account created successfully! Please log in.', 'success')
    return redirect(url_for('user.login_form'))


@user_bp.get('/login')
def login_form():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('user/login.html')


@user_bp.post('/login')
def login():
    email = (request.form.get('email') or '').strip()
    password = request.form.get('password') or ''
    if not email or not password:
        flash('Email and password are required.', 'danger')
        return redirect(url_for('user.login_form'))
    user = user_service.authenticate(email=email, password=password)
    if user:
        login_user(user)
        token = generate_token(user.id)
        response = make_response(redirect(url_for('main.index')))
        max_age = current_app.config['JWT_EXPIRATION_HOURS'] * 3600
        response.set_cookie(
            'jwt_token',
            token,
            httponly=True,
            samesite='Lax',
            secure=not current_app.debug,
            max_age=max_age,
        )
        flash(f'Welcome back, {user.full_name}!', 'success')
        return response
    flash('Invalid email or password.', 'danger')
    return redirect(url_for('user.login_form'))


@user_bp.get('/logout')
@login_required
def logout():
    logout_user()
    response = make_response(redirect(url_for('user.login_form')))
    response.delete_cookie('jwt_token')
    flash('You have been logged out.', 'success')
    return response
