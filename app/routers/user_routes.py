<<<<<<< HEAD
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services import user_service
=======
from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, current_app
from flask_login import login_user, logout_user, login_required

from app.services import user_service
from app.jwt_utils import generate_token
>>>>>>> origin/kanan

user_bp = Blueprint('user', __name__)


@user_bp.get('/register')
def register_form():
    return render_template('user/register.html')


@user_bp.post('/register')
def register():
<<<<<<< HEAD
    user, access_token, error = user_service.register_user(
        full_name=request.form.get('full_name'),
        email=request.form.get('email'),
        password=request.form.get('password'),
        role=request.form.get('role', 'user'),
    )
    if error:
        flash(error)
        return redirect(url_for('user.register_form'))
    flash('Account created successfully! Welcome aboard!', 'success')
    # Set JWT token in httpOnly cookie and redirect
    response = redirect(url_for('main.index'))
    response.set_cookie('access_token_cookie', access_token, httponly=True, secure=False, samesite='Lax')
    return response
=======
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
>>>>>>> origin/kanan


@user_bp.get('/login')
def login_form():
    return render_template('user/login.html')


@user_bp.post('/login')
def login():
<<<<<<< HEAD
    user, access_token = user_service.authenticate(
        email=request.form.get('email'),
        password=request.form.get('password'),
    )
    if user and access_token:
        flash(f'Welcome back, {user.full_name}!', 'success')
        # Set JWT token in httpOnly cookie and redirect
        response = redirect(url_for('main.index'))
        response.set_cookie('access_token_cookie', access_token, httponly=True, secure=False, samesite='Lax')
        return response
    flash('Invalid email or password.')
=======
    user = user_service.authenticate(
        email=request.form.get('email'),
        password=request.form.get('password'),
    )
    if user:
        login_user(user)
        token = generate_token(user.id)
        response = make_response(redirect(url_for('main.index')))
        max_age = current_app.config['JWT_EXPIRATION_HOURS'] * 60 * 60
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
>>>>>>> origin/kanan
    return redirect(url_for('user.login_form'))


@user_bp.get('/logout')
<<<<<<< HEAD
def logout():
    flash('You have been logged out.', 'success')
    # Remove JWT token cookie and redirect
    response = redirect(url_for('user.login_form'))
    response.delete_cookie('access_token_cookie')
=======
@login_required
def logout():
    logout_user()
    response = make_response(redirect(url_for('user.login_form')))
    response.delete_cookie('jwt_token')
    flash('You have been logged out.', 'success')
>>>>>>> origin/kanan
    return response
