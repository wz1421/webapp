from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

import enum

db = SQLAlchemy()

class Gender(enum.Enum):
    male = 0
    female = 1

    def __str__(self):
        return '%s' % self.name

class BabyCategory(enum.Enum):
    premature = 0
    mat_diabetic = 1
    small = 2

    def __str__(self):
        return '%s' % self.name

class UserCategory(enum.Enum):
    doctor = 0
    nurse = 1
    researcher = 2
    admin = 3

    def __str__(self):
        return '%s' % self.name

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
    g_age = db.Column(db.Integer, nullable=False)
    med_conds = db.Column(db.String, nullable=True)
    curr_meds = db.Column(db.String, nullable=True)
    category = db.Column(db.Enum(BabyCategory), nullable=False)
    comments = db.Column(db.Text, nullable=True)
    doctor_email = db.Column(
        db.String,
        db.ForeignKey("user.email"),
        nullable=False
    )
    doctor_in_charge = db.relationship("User", back_populates="babies")

# Mapping of form element names to pretty-printed titles
field_titles = {
    "nigel_number": "1a. NIGEL Number",
    "gender": "1b. Gender",
    "dob": "1c. Date of Birth",
    "birth_weight": "1d. Birth Weight (g)",
    "birth_length": "1e. Birth Length (cm)",
    "doctor_email": "2a. Doctor in Charge",
    "g_age": "3a. Gestational Age",
    "med_conds": "3b. Existing Medical Conditions",
    "curr_meds": "3c. Current In-use Medications",
    "category": "4a. Baby Category",
    "comments": "5a. Additional Comments",
}

# Mapping of baby categories to pretty-printed titles
baby_category_titles = {
    "premature": "Premature",
    "matDiabetic": "Maternal Diabetic",
    "small": "Small Baby"
}
