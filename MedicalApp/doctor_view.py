from flask import (Blueprint, render_template, redirect,
                   flash, url_for, request, abort)
from .user import User
from .db.dbmanager import get_db
from oracledb import InternalError, DatabaseError
from flask_login import login_user, logout_user, login_required
from .forms import AppointmentResponseForm

bp = Blueprint('doctor', __name__, url_prefix="/doctor/")


@bp.route('/')
# @login_required
def dashboard():
    return render_template("doctor.html")


@bp.route('/appointments/')
# @login_required
def confirmed_appointments():
    try:
        appointments = get_db().get__appointments_by_status(1)
        if appointments is None or len(appointments) == 0:
            flash("No confirmed appointments")
            return redirect(url_for('doctor.dashboard'))
        return render_template('doctor_appointments.html', appointments=appointments)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))


@bp.route('/requests/')
# @login_required
def requested_appointments():
    try:
        appointments = get_db().get_appointments_by_status(0)
        if appointments is None or len(appointments) == 0:
            flash("No requested appointments")
            return redirect(url_for('doctor.dashboard'))
        return render_template('doctor_requests.html', appointments=appointments)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))


@bp.route('/requests/<int:id>/', methods=['GET', 'POST'])
# @login_required
def update_appointment(id):
    form = AppointmentResponseForm()
    appointment = get_db().get_appointment_by_id(id)

    if request.method == 'POST' and form.validate_on_submit():
        status = form.select_confirmation.data
        try:
            get_db().update_appointment_status(id, status)
            flash("Appointment has been successfully updated")
            return redirect(url_for('doctor.requested_appointments'))
        except DatabaseError:
            flash("Something went wrong with the database")
            return redirect(url_for('doctor.requested_appointments'))

    if appointment is None:
        abort(404, "This address does not exist")
    return render_template('requested_appointment.html', appointment=appointment, form=form)

@bp.route('/patients/')
# @login_required
def patients():
    try:
        patients = get_db().get_patients_by_doctor(DOCTOR_ID)
        if patients is None or len(patients) == 0:
            flash("No patients are currently being supervised by you")
            return redirect(url_for('doctor.dashboard'))
        return render_template('doctor_patients.html', patients=patients)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))

@bp.route('/notes/<int:patient_id>')
# @login_required
def notes(patient_id):
    try:
        notes = get_db().get_notes_by_patient_id(patient_id)
        if notes is None or len(notes) == 0:
            flash("No notes are currently written for this patient")
            return redirect(url_for('doctor.dashboard'))
        return render_template('patient_notes.html', notes=notes)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))