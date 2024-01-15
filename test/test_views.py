import pytest
from flask import Flask, url_for
from Website import create_app, db
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

def test_home_authenticated(client):
    unique_email3 = generate_unique_email()
    with client.application.app_context():
        user = User(
            email=unique_email3,
            first_name='User',
            password='password',
            category=UserCategory.doctor,
        )
        db.session.add(user)
        db.session.commit()

    # Perform login
    response = client.post('/login', data={
        'email': unique_email3,
        'password': 'password',
    }, follow_redirects=True)  # Ensure that you follow redirects

    assert response.status_code == 200  # OK status code


def test_home_unauthenticated(client):
    response = client.get('/', follow_redirects=False)
    assert response.status_code == 302  # Redirect status code

def test_baby_data_route(client):
    # Log in as the registered admin user
    client.post('/login', data={'email': 'admin@ic.ac.uk', 'password': 'admin'},follow_redirects=True)

    # Access the /babydata route
    response = client.get('/babydata')
    assert response.status_code == 200  # Ensure that the response is OK (200)

def test_add_baby_info_route(client):
    # Log in as the registered admin user
    client.post('/login', data={'email': 'admin@ic.ac.uk', 'password': 'admin'}, follow_redirects=True)

    # Access the /add-baby-info route
    response = client.get('/add-baby-info')
    assert response.status_code == 200  # Ensure that the response is OK (200)
    assert b'Add baby information' in response.data

def test_add_med_history_route(client):
    # Log in as the registered admin user
    client.post('/login', data={'email': 'admin@ic.ac.uk', 'password': 'admin'}, follow_redirects=True)

    # Access the /add-med-history route
    response = client.get('/add-med-history')
    assert response.status_code == 200  # Ensure that the response is OK (200)
    assert b'Add baby information' in response.data

def test_success_route(client):
    # Log in as the registered admin user
    client.post('/login', data={'email': 'admin@ic.ac.uk', 'password': 'admin'}, follow_redirects=True)

    # Access the /success route
    response = client.get('/success')
    assert response.status_code == 200  # Ensure that the response is OK (200)
    assert b'Success' in response.data

def test_plot_route(client):
    # Log in as the registered admin user
    client.post('/login', data={'email': 'admin@ic.ac.uk', 'password': 'admin'}, follow_redirects=True)

    # Access the /plot-plot route
    response = client.get('/plot-plot')
    assert response.status_code == 200  # Ensure that the response is OK (200)


def test_baby_categories_route(client):
    # Log in as the registered admin user
    client.post('/login', data={'email': 'admin@ic.ac.uk', 'password': 'admin'}, follow_redirects=True)

    # Access the /baby-categories route
    response = client.get('/baby-categories')
    assert response.status_code == 200  # Ensure that the response is OK (200)


def test_premature_baby_route(client):
    # Log in as the registered admin user
    client.post('/login', data={'email': 'admin@ic.ac.uk', 'password': 'admin'}, follow_redirects=True)

    # Access the /premature-baby route
    response = client.get('/baby-categories/premature-baby')
    assert response.status_code == 200  # Ensure that the response is OK (200)

def test_infant_of_diabetic_mother_route(client):
    # Log in as the registered admin user
    client.post('/login', data={'email': 'admin@ic.ac.uk', 'password': 'admin'}, follow_redirects=True)

    # Access the /infant-of-diabetic-mother route
    response = client.get('/baby-categories/infant-of-diabetic-mother')
    assert response.status_code == 200  # Ensure that the response is OK (200)

def test_small_baby_route(client):
    # Log in as the registered admin user
    client.post('/login', data={'email': 'admin@ic.ac.uk', 'password': 'admin'}, follow_redirects=True)

    # Access the /small-baby route
    response = client.get('/baby-categories/small-baby')
    assert response.status_code == 200  # Ensure that the response is OK (200)


