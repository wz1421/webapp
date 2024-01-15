# Storing standard routes for the website
from flask import Blueprint, render_template, redirect, url_for, request, session, json, flash
from flask_login import login_required, current_user
from datetime import datetime

from . import db
from .models import ActivityLog, ActivityCategory, Baby, BabyCategory, GlucoseRecord, User, UserCategory, field_titles, baby_category_titles

# Blueprint for non-authentication-related routes
views = Blueprint('views', __name__)

@views.route('/')
def home():
    """ Route for the home page. Redirects to login page if the user is not authenticated."""
    if current_user.is_authenticated:
        return render_template("view/home.html")
    else:
        return redirect(url_for("auth.login"))

@views.route('/babydata')
@login_required
def baby_data():
    """ Route for displaying baby data. Requires authentication. """
    return render_template("categories/baby_categories.html",text="Baby 1")

@views.route('/add-baby-info', methods=['GET','POST'])
@login_required
def add_baby_info():
    """ Route for adding baby information. Stores information in session and redirects to add medical history."""
    baby_information = session.get("baby_information", {})
    passed_baby_information = request.args.get('baby_information')
    if passed_baby_information:
        baby_information = json.loads(passed_baby_information)
    if request.method =='POST':
        print("matching baby:", Baby.query.filter_by(nigel_number=request.form["nigel_number"]).all())
        # TODO: Change admin to doctor; this is currently done for convenience
        if not User.query.filter_by(email=request.form["doctor_email"], category=UserCategory.admin).first():
            flash("Doctor's email is invalid", category="error")
        elif Baby.query.filter_by(nigel_number=request.form["nigel_number"]).first():
            flash("NIGEL number is already registered", category="error")
        else:
            session['baby_information'] = request.form.to_dict()
            return redirect(url_for('views.add_med_history'))

    return render_template("updates/add_baby_info.html", baby_information=baby_information)

@views.route('/add-med-history', methods=['GET','POST'])
@login_required
def add_med_history():
    """ Route for adding medical history. Stores information in session and redirects to review information."""
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
    """ Route for reviewing information before submission. Clears session data on successful submission."""
    baby_information = session.get('baby_information', {})
    medical_history = session.get('medical_history', {})

    # Form data to be passed to the /review-info route
    form_data = {
        'Baby Information': {field_titles[k]: v for (k, v) in baby_information.items()},
        'Medical History': {field_titles[k]: v for (k, v) in medical_history.items()},
    }

    print(form_data["Medical History"])

    form_data["Medical History"][field_titles["category"]] = (
        baby_category_titles[form_data["Medical History"][field_titles["category"]]]
    )

    # Combine medical_history with baby_information and convert DOB to datetime
    # This is for creating the new baby efficiently

    combined_dict = dict(baby_information)
    combined_dict.update(medical_history)
    combined_dict["dob"] = datetime.strptime(
        combined_dict["dob"], "%Y-%m-%d"
    ).date()

    if request.method =='POST':
        session.pop('baby_information', None)
        session.pop('medical_history', None)

        db.session.add(Baby(**combined_dict))
        db.session.add(ActivityLog(
            user_id = current_user.id,
            baby_id = combined_dict["nigel_number"],
            type = ActivityCategory.register,
            timestamp = datetime.now()
        ))
        db.session.commit()

        return redirect(url_for('views.success'))
    elif 'back_to_baby_info' in request.args:  # Check for back button press
        return redirect(url_for('views.add_baby_info', baby_information=json.dumps(baby_information)))

    return render_template('updates/review_info.html', form_data=form_data)

@views.route('/success',  methods=['GET','POST'])
@login_required
def success():
    """ Route for displaying a success page. Redirects to home page on button click."""
    if request.method == 'POST':
        return redirect(url_for('views.home'))
    return render_template("view/success.html")

@views.route('/plot-plot', methods=['GET', 'POST'])
@login_required
def plot():
    if 'back_to_prev_cat' in request.args:
        if 'current_cat' in session:
            return redirect(session['current_cat'])

    """ Route for displaying a plot."""
    return render_template("plotplot.html")

@views.route('/save-plot', methods=['POST'])
def save_plot():
    """ Route that simply saves a plot to the database. This is done in the
     background using jQuery and AJAX. """
    try:
        plot_data = request.json
    except:
        plot_data = request.form

    db.session.add(GlucoseRecord(**plot_data))
    db.session.add(ActivityLog(
        user_id = current_user.id,
        baby_id = plot_data["baby_id"],
        type = ActivityCategory.record,
        timestamp = datetime.now()
    ))
    db.session.commit()
    print("Saved:", GlucoseRecord.query.all())
    return "Successfully stored glucose record"

@views.route('/view-records')
@login_required
def view_records():
    """ View the records of the baby given in the URL args. """
    
    # Can assume the baby exists since this route is only accessed through a
    # valid link for a specific baby
    nigel_number = int(request.args["nigel"])
    baby_data = Baby.query.filter_by(nigel_number=nigel_number).first().to_dict()

    db.session.add(ActivityLog(
        user_id = current_user.id,
        baby_id = nigel_number,
        type = ActivityCategory.view,
        timestamp = datetime.now()
    ))
    db.session.commit()

    records = GlucoseRecord.query.filter_by(baby_id=nigel_number).all()
    records = [record.to_dict() for record in records]

    return render_template("view_records.html", data=baby_data, titles=field_titles, records=records)

@views.route('/baby-categories', methods=['GET','POST'])
@login_required
def baby_categories():
    """ Route for displaying baby category."""
    return render_template('categories/baby_categories.html')

@views.route('/baby-categories/premature-baby', methods=['GET','POST'])
@login_required
def premature_baby():
    session['current_cat'] = url_for('views.premature_baby')

    """ Route for displaying information of premature baby, with a back button"""
    if 'back_to_baby_cat' in request.args:
        return redirect(url_for('views.baby_categories'))
    
    babies = Baby.query.filter_by(category=BabyCategory.premature).all()

    return render_template("categories/category_page.html", category="Premature Baby", babies=babies)

@views.route('/baby-categories/infant-of-diabetic-mother', methods=['GET','POST'])
@login_required
def infant_of_diabetic_mother():
    session['current_cat'] = url_for('views.infant_of_diabetic_mother')

    """ Route for displaying information of infant of diabetic mother, with a back button"""
    if 'back_to_baby_cat' in request.args:
         return redirect(url_for('views.baby_categories'))
    babies = Baby.query.filter_by(category=BabyCategory.mat_diabetic).all()

    return render_template("categories/category_page.html", category="Infant Of Diabetic Mother", babies=babies)

@views.route('/baby-categories/small-baby', methods=['GET','POST'])
@login_required
def small_baby():
    session['current_cat'] = url_for('views.small_baby')

    """ Route for displaying information of small baby, with a back button"""
    if 'back_to_baby_cat' in request.args:
         return redirect(url_for('views.baby_categories'))
    
    babies = Baby.query.filter_by(category=BabyCategory.small).all()

    return render_template("categories/category_page.html", category="Small Baby", babies=babies)

