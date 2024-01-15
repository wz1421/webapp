import pytest
from flask import Flask, url_for
from Website import create_app, db  # Adjust the import path as needed
from Website.models import User, UserCategory
import time
import random

def generate_unique_email():
    timestamp = int(time.time())
    random_suffix = random.randint(1, 1000)
    return f'user_{timestamp}_{random_suffix}@example.com'

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True  # Set the app to testing mode
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
    # Use an SQLite in-memory database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():  # Create an application context
            db.create_all()  # Create the database tables
            user = User(
                email='user@example.com',
                first_name='User',
                password='password',
                category=UserCategory.doctor,
            )
            db.session.add(user)
            db.session.commit()
        yield client


def test_signup_redirect(client):
    response = client.post('/signup', data={
        'email': 'newuser@example.com',
        'firstName': 'New User',
        'password1': 'password',
        'password2': 'password',
    }, follow_redirects=False)

    assert response.status_code == 302  # Redirect status code

def test_login_success_redirect(client):
    unique_email = generate_unique_email()
    with client.application.app_context():
        user = User(
            email=unique_email,
            first_name='User',
            password='password',
            category=UserCategory.doctor,
        )
        db.session.add(user)
        db.session.commit()

    response = client.post('/login', data={
        'email': 'user@example.com',
        'password': 'password',
    }, follow_redirects=False)

    assert response.status_code == 302  # Redirect status code

def test_login_failure_redirect(client):
    response = client.post('/login', data={
        'email': 'nonexistent@example.com',
        'password': 'password',
    }, follow_redirects=False)

    assert response.status_code == 302  # Redirect status code

def test_logout_redirect(client):
    unique_email2 = generate_unique_email()
    with client.application.app_context():
        user = User(
            email=unique_email2,
            first_name='User',
            password='password',
            category=UserCategory.doctor,
        )
        db.session.add(user)
        db.session.commit()

        # Perform login
        client.post('/login', data={
            'email': unique_email2,
            'password': 'password',
        })

        # Perform logout
        response = client.get('/logout', follow_redirects=False)
        assert response.status_code == 302  # Redirect status code