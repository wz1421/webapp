# Storing standard routes for the website
from flask import Blueprint, render_template

#Blueprint of our application
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")
@views.route('/babydata')
def babydata():
    return render_template("babydata.html")
