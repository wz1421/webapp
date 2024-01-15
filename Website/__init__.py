from flask import Flask
from flask_login import LoginManager, logout_user
from werkzeug.security import generate_password_hash

from .models import db, User, Baby, BabyCategory, Gender, UserCategory
from .views import views
from .auth import auth
from .admin import admin

DB_NAME = "database.db"

def register_admin(db):
    """Register a hospital administrator user that can create new accounts."""
    admin_user = User(
        email="admin@ic.ac.uk",
        first_name="DefaultAdministrator",
        password=generate_password_hash("admin"),
        category=UserCategory.admin
    )

    db.session.add(admin_user)
    db.session.commit()

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
        register_admin(db)

    # Initialise login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(email):
        return User.query.get(email)

    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    return app
