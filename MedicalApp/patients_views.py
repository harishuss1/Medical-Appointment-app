from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from MedicalApp.forms import PatientDetailsForm
from MedicalApp.user import MedicalPatient
from .db.dbmanager import get_db
# from .forms import PatientForm   will implement this later for updating

bp = Blueprint('patient', __name__, url_prefix="/patients")


@bp.route('/')
@login_required
def patient_dashboard():
    if current_user.access_level != 'PATIENT':
        flash("You do not have permission to access this page.")
        return redirect(url_for('home.index'))

    appointments = get_db().get_patient_appointments(current_user.id)
    return render_template('patient_dashboard.html', appointments=appointments)


@bp.route('/appointments')
@login_required
def view_appointments():
    if current_user.access_level != 'PATIENT':
        flash("You do not have permission to access this page.")
        return redirect(url_for('home.index'))

    appointments = get_db().get_patient_appointments(current_user.id)
    return render_template('patient_appointments.html', appointments=appointments)


@bp.route('/details/update', methods=['GET', 'POST'])
@login_required
def update_patient():
    if current_user.access_level != 'PATIENT':
        flash("You do not have permission to access this page.")
        return redirect(url_for('home.index'))

    form = PatientDetailsForm()

    if request.method == 'POST' and form.validate_on_submit():
        dob = form.dob.data
        blood_type = form.blood_type.data
        height = form.height.data
        weight = form.weight.data

        get_db().update_patient_details(current_user.id, dob, blood_type, height, weight)

        flash('Your information has been updated.')
        return redirect(url_for('patient.view_patient'))

    return render_template('update_patient.html', form=form)


@bp.route('/details', methods=['GET'])
@login_required
def view_patient():
    if current_user.access_level != 'PATIENT':
        flash("You do not have permission to access this page.")
        return redirect(url_for('home.index'))

    patient_details = get_db().get_patient_details(current_user.id)

    if patient_details is None:
        flash("No patient details found.")
        return redirect(url_for('home.index'))

    patient = MedicalPatient(weight=patient_details.weight, email=patient_details.email, password=patient_details.password, first_name=patient_details.first_name, last_name=patient_details.last_name,
                             access_level=patient_details.access_level, dob=patient_details.dob, blood_type=patient_details.blood_type, height=patient_details.height, avatar_path=patient_details.avatar_path, id=patient_details.id)

    return render_template('patient_details.html', patient=patient)
