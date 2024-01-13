# Storing standard routes for the website
from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import login_required, current_user
from .db import db, Baby

#Blueprint of our application
views = Blueprint('views', __name__)

@views.route('/')
def home():
    if current_user.is_authenticated:
        return render_template("view/home.html")
    else:
        return redirect(url_for("auth.login"))

@views.route('/babydata')
@login_required
def baby_data():
    return render_template("view/babydata.html",text="Baby 1")

@views.route('/add-baby-info', methods=['GET','POST'])
@login_required
def add_baby_info():
    baby_information = session.get("baby_information", {})
    passed_baby_information = request.args.get('baby_information')
    if passed_baby_information:
        baby_information = json.loads(passed_baby_information)
    if request.method =='POST':
        session['baby_information'] = request.form.to_dict()
        return redirect(url_for('views.add_med_history'))

    return render_template("updates/add_baby_info.html", baby_information=baby_information)

@views.route('/add-med-history', methods=['GET','POST'])
@login_required
def add_med_history():
    medical_history = session.get('medical_history', {})
    passed_medical_history = request.args.get('medical_history')
    if passed_medical_history:
        medical_history = json.loads(passed_medical_history)
    if request.method =='POST':
        session['medical_history'] = request.form.to_dict()
        return redirect(url_for('views.review_info'))
    return render_template("updates/add_med_history.html", medical_history=medical_history)

@views.route('/review-info', methods=['GET','POST'])
@login_required
def review_info():
    baby_information = session.get('baby_information', {})
    medical_history = session.get('medical_history', {})

    form_data = {
        'Baby Information': baby_information,
        'Medical History': medical_history,
    }
    if request.method =='POST':
        session.pop('baby_information', None)
        session.pop('medical_history', None)
        return redirect(url_for('views.success'))
    elif 'back_to_baby_info' in request.args:  # Check for back button press
        return redirect(url_for('views.add_baby_info', baby_information=json.dumps(baby_information)))
    else:
        return render_template('updates/review_info.html', form_data=form_data)

@views.route('/success',  methods=['GET','POST'])
@login_required
def success():
    if request.method == 'POST':
        return redirect(url_for('views.home'))
    return render_template("view/success.html")

@views.route('/plot-plot', methods=['GET', 'POST'])
@login_required
def plot():
    return render_template("plotplot.html")


@views.route('/baby-categories', methods=['GET','POST'])
@login_required
def baby_categories():
    return render_template('categories/baby_categories.html')

@views.route('/premature-baby', methods=['GET','POST'])
@login_required
def premature_baby():
    if 'back_to_baby_cat' in request.args:
        return redirect(url_for('views.baby_categories'))
    return render_template("categories/prematureBaby.html")

@views.route('/infant-of-diabetic-mother', methods=['GET','POST'])
@login_required
def infant_of_diabetic_mother():
    if 'back_to_baby_cat' in request.args:
         return redirect(url_for('views.baby_categories'))
    return render_template("categories/infantOfDiabeticMother.html")

@views.route('/small-baby', methods=['GET','POST'])
@login_required
def small_baby():
    if 'back_to_baby_cat' in request.args:
         return redirect(url_for('views.baby_categories'))
    return render_template("categories/smallBaby.html")

