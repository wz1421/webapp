from flask import (Blueprint, render_template, request, flash, redirect,
                  url_for, session, json)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from . import db
from .models import User, UserCategory

# Blueprint grouping administrator routes together
admin = Blueprint('admin', __name__)

# Being logged in is required for signing up because only an administrator
# can create new user accounts
@admin.route('/signup')
@login_required
def sign_up():
    if current_user.category == UserCategory.admin:
        return render_template("login_signup/sign_up.html")
    else:
        return redirect(url_for("views.home.html"))

@admin.route('/signup', methods=['POST'])
@login_required
def sign_up_post():
    if current_user.category != UserCategory.admin:
        return redirect(url_for("views.home"))

    email = request.form.get('email', "")
    first_name = request.form.get('firstName', "")
    password1 = request.form.get('password1', "")
    password2 = request.form.get('password2', "")

    if len(email) < 4:
        flash('Invalid email address.', category='error')
    elif User.query.filter_by(email=email).first():
        flash('User with this email already exists.', category='error')
    elif len(first_name) == 0:
        flash('Please enter your name', category='error')
    elif password1 != password2:
        flash('Passwords don\'t match.', category='error')
    elif len(password1) < 7:
        flash('Password must be at least 7 characters', category='error')
    else:
        new_user = User(
            email=email,
            first_name=first_name,
            password=generate_password_hash(password1),
            category=UserCategory.doctor
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created! Welcome.', category='success')
        return redirect(url_for("views.home"))
    return redirect(url_for("admin.sign_up"))