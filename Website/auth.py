#storing standard routes for the website
from flask import Blueprint, render_template , request , flash

#Blueprint of our applicatio-auth blue print
auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    #way to add texts to the page
    #adding if statements
    return render_template("login.html", text="Please log in with your work email",boolean=True)

@auth.route('/babydata')
def baby_data():
    return render_template(baby_data.html,text="Baby 1")

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method =="POST":
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #can use this to prevent unauthorised personnel from signing up
        if len(email) < 4:
            flash('Unauthorised to signup for an account.', category='error')
        elif len(firstName) < 1:
            flash('Please enter your name', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            #add user to database
            flash('Account created! Welcome.', category='success')
    return render_template("sign_up.html")
    #submit button on the sign up page is a post request
    data = request.form
    print(data) #access info from the server that s been submitted
    return render_template("sign_up.html")

