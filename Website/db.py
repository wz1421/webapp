from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from .db_enums import BabyCategory, Gender, UserCategory

db = SQLAlchemy()

# Databse schema
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    category = db.Column(db.Enum(UserCategory), nullable=False)
    babies = db.relationship("Baby", back_populates="doctor_in_charge")

class Baby(db.Model):
    __tablename__ = "baby"
    id = db.Column(db.Integer, primary_key=True)
    nigel_number = db.Column(db.Integer, unique=True, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    birth_weight = db.Column(db.Float, nullable=False)
    birth_length = db.Column(db.Float, nullable=False)
    category = db.Column(db.Enum(BabyCategory), nullable=False)
    doctor_email = db.Column(
        db.String,
        db.ForeignKey("user.email"),
        nullable=False
    )
    doctor_in_charge = db.relationship("User", back_populates="babies")
