from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services import user_service

user_bp = Blueprint('user', __name__)


@user_bp.get('/register')
def register_form():
    return render_template('user/register.html')


@user_bp.post('/register')
def register():
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


@user_bp.get('/login')
def login_form():
    return render_template('user/login.html')


@user_bp.post('/login')
def login():
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
    return redirect(url_for('user.login_form'))


@user_bp.get('/logout')
def logout():
    flash('You have been logged out.', 'success')
    # Remove JWT token cookie and redirect
    response = redirect(url_for('user.login_form'))
    response.delete_cookie('access_token_cookie')
    return response
