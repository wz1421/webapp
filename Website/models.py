#creating data base models for users and baby data
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    #unqiue id
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    #gets the current date and time
    #can use it to store the baby data
    date = db.Column(db.DateTime(timezone=True), default =func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    #maximum string of email is 150
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))