from flask import (Blueprint, render_template, request, flash, redirect,
                  url_for, session, json)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from . import db
from .models import User, UserCategory

# Blueprint grouping authentication routes together
auth = Blueprint('auth', __name__)
    

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', "")
        password = request.form.get('password', "")

        user = User.query.filter_by(email=email).first()
        print("EMAIL", email, "USER", user)

        if not user or not check_password_hash(user.password, password):
            flash("Incorrect credentials. Please try again.")
            return redirect(url_for("auth.login"))

        # Credentials match
        login_user(user)
        return redirect(url_for("views.baby_data"))

    return render_template("login_signup/login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

# Being logged in is required for signing up because only an administrator
# can create new user accounts
@auth.route('/signup')
@login_required
def sign_up():
    if current_user.category == UserCategory.admin:
        return render_template("login_signup/sign_up.html")
    else:
        return redirect(url_for("views.home.html"))

@auth.route('/signup', methods=['POST'])
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
    return redirect(url_for("auth.signup"))
