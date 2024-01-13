from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .db import db, User, Baby
from .db_enums import BabyCategory, Gender, UserCategory
from .views import views
from .auth import auth

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    #incripts and secure the cookie and session data realted to our website
    app.config['SECRET_KEY'] = 'sugar babies'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Create the database from scratch
    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app
