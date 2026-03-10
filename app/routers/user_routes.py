from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_user, logout_user, login_required

from app.services import user_service
from app.jwt_utils import generate_token

user_bp = Blueprint('user', __name__)


@user_bp.get('/register')
def register_form():
    return render_template('user/register.html')


@user_bp.post('/register')
def register():
    # role həmişə 'user' — formdan gəlmir (task #4)
    user, error = user_service.register_user(
        full_name=request.form.get('full_name'),
        email=request.form.get('email'),
        password=request.form.get('password'),
        role='user',  # ← həmişə user, admin ola bilməz
    )
    if error:
        flash(error, 'danger')
        return redirect(url_for('user.register_form'))
    flash('Account created successfully! Please log in.', 'success')
    return redirect(url_for('user.login_form'))


@user_bp.get('/login')
def login_form():
    return render_template('user/login.html')


@user_bp.post('/login')
def login():
    user = user_service.authenticate(
        email=request.form.get('email'),
        password=request.form.get('password'),
    )
    if user:
        login_user(user)
        token = generate_token(user.id)
        response = make_response(redirect(url_for('main.index')))
        response.set_cookie('jwt_token', token, httponly=True, samesite='Lax')
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
