from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"
def create_app():
    app = Flask(__name__)
    #incripts and secure the cookie and session data realted to our website
    app.config['SECRET_KEY'] = 'sugar babies'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    return app
def create_database(app): #check if data base exist, if it doesnt, create it
    if not path.exists('webiste/'+DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

