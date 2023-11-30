#storing standard routes for the website
from flask import Blueprint, render_template

#Blueprint of our applicatio-auth blue print
auth = Blueprint('auth',__name__)

@auth.route('/login')
def login():
    #way to add texts to the page
    #adding if statements
    return render_template("login.html", text="Please log in with your work email",boolean=True)

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up')
def sign_up():
    return render_template("sign_up.html")

