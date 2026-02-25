from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models.user_model import User

user_bp = Blueprint('user', __name__)


def _email_already_exists(email):
    return User.query.filter_by(email=email).first() is not None


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'user')

        if _email_already_exists(email):
            flash('An account with this email already exists.', 'danger')
            return redirect(url_for('user.register'))

        new_user = User(
            full_name=full_name,
            email=email,
            password=generate_password_hash(password),
            role=role,
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('user.login'))

    return render_template('user/register.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(url_for('main.index'))

        flash('Invalid email or password.', 'danger')
        return redirect(url_for('user.login'))

    return render_template('user/login.html')


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('user.login'))
