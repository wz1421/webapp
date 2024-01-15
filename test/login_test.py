import pytest
from flask import Flask, url_for, request
from flask_login import LoginManager, current_user, login_user
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Website.auth import auth
from Website.db import db, User


def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'sugar babies'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Set your database URI here
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
    app.config['SERVER_NAME'] = 'localhost.localdomain'  # Dummy value for SERVER_NAME
    app.register_blueprint(auth)
    db.init_app(app)
    # Initialize the LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Replace 'auth.login' with the actual login route name
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()  # Create the tables in the test database

    return app


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_login_template(client):
    with client:
        response = client.get('login_signup/login')

        # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    assert b"Login" in response.data


def test_login_successful(client):
    with client:
        user = User.query.first()
        if user is None:
            print("No user found in the database.")
            return  # Stop the test and investigate why no user is found

        print(f"Found user: {user.email} (ID: {user.id})")

        with client.session_transaction() as sess:
            sess['user_id'] = user.id
        response = client.post(url_for('auth.login'), data={'email': 'admin@ic.ac.uk', 'password': 'admin'})
    assert response.status_code == 302
    assert current_user == user


def test_login_invalid_credentials(client):
    response = client.post(url_for('auth.login'), data={'email': 'invalid@example.com', 'password': 'invalid_password'})

    assert response.status_code == 200  # Login page should be displayed again
    assert b"Invalid email or password" in response.data


def test_login_empty_fields(client):
    response = client.post(url_for('auth.login'), data={'email': '', 'password': ''})

    assert response.status_code == 200  # Login page should be displayed again
    assert b"Field is required" in response.data


