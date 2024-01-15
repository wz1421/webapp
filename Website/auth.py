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
