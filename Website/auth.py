#storing standard routes for the website
from flask import Blueprint, render_template, request, flash, redirect, url_for, session

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
            flash('Unauthorised to sign up for an account, must be authorisied staff of the hospital.', category='error')
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

@auth.route('/add-baby-info', methods=['GET','POST'])
def add_baby_info():
    if request.method =='POST':
        session['baby_information'] = request.form.to_dict()
        return redirect(url_for('auth.add_med_history'))

    return render_template("add_baby_info.html")

@auth.route('/add-med-history', methods=['GET','POST'])
def add_med_history():
    if request.method =='POST':
        session['medical_history'] = request.form.to_dict()
        return redirect(url_for('auth.review_info'))
    return render_template("add_med_history.html")

@auth.route('/review-info', methods=['GET','POST'])
def review_info():
    baby_information = session.get('baby_information', {})
    medical_history = session.get('medical_history', {})

    form_data = {
        'Baby Information': baby_information,
        'Medical History': medical_history,
    }
    if request.method =='POST':
        return redirect(url_for('auth.success'))
    return render_template('review_info.html',  form_data=form_data)

@auth.route('/success')
def success():
    return render_template("success.html",text="Baby 1")

@auth.route('/baby-categories', methods=['GET','POST'])
def baby_categories():
    return render_template('baby_categories.html')

@auth.route('/premature-baby', methods=['GET','POST'])
def premature_baby():
    return render_template("prematureBaby.html")

@auth.route('/infant-of-diabetic-mother', methods=['GET','POST'])
def infant_of_diabetic_mother():
    return render_template("infantOfDiabeticMother.html")

@auth.route('/small-baby', methods=['GET','POST'])
def small_baby():
    return render_template("smallBaby.html")
