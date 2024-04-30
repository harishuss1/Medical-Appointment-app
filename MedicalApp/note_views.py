import os
import shutil
import tempfile
from zipfile import ZipFile
from flask import (Blueprint, after_this_request, current_app, render_template, redirect,
                   flash, send_file, url_for, request, abort)
from .user import User
from .db.dbmanager import get_db
from oracledb import InternalError, DatabaseError
from flask_login import current_user, login_user, logout_user, login_required
from .forms import NoteForm
from .db.db import Database
from .note import Note

bp = Blueprint('note', __name__, url_prefix="/notes/")

@bp.route('/<int:note_id>/')
@login_required
def note(note_id):
    note = get_db().get_note_by_id(note_id)
    if note == None:
        flash("no note available")
        return redirect(url_for('note.notes', user_id=current_user.id))
    return render_template('note.html', note=note)

@bp.route('/note/<int:user_id>/')
@login_required
def notes(user_id):
    if current_user.access_level != 'STAFF' and current_user.access_level != 'PATIENT':
        return redirect(url_for('home.index'))
    notes = None
    try:
        #<dd><a href="{{ url_for('note.notes', user_id=patient.id) }}">See notes.</a></dd> what to do about this...
        #CHANGE TO RELATIVE PATH
        if current_user.access_level == 'STAFF':
            notes = get_db().get_notes_by_doctor_id(user_id)
        else:
            notes = get_db().get_notes_by_patient_id(user_id)
        if notes is None or len(notes) == 0:
            flash("No notes are currently written for this user")
    except DatabaseError as e:
        flash("Something went wrong with the database")
    return render_template('notes.html', notes=notes)
    
@bp.route('/add/', methods=['GET', 'POST'])
@login_required
def add():
    if current_user.access_level != 'STAFF':
        return redirect('home.index')
    form = NoteForm()
    form.set_choices()
    if request.method == 'POST' and form.validate_on_submit():
        files = form.attachement.data
        paths = []
        for file in files:
            filename = file.filename
            folder = os.path.join(current_app.config['ATTACHEMENTS'], form.patient.data)
            if not os.path.exists(folder):
                os.makedirs(folder)
            path = os.path.join(folder, filename)
            path = os.path.relpath(path, start=os.curdir) 
            paths.append(path)
            file.save(path) #actually adds it to the directory
        
        patient = get_db().get_patients_by_id(form.patient.data)
        #form.date.data.strftime('%Y-%m-%d')
        note = Note(patient, current_user, form.date.data, form.note.data, paths)
        
        get_db().create_note(note)
        return redirect(url_for('note.notes', user_id=current_user.id))
    return render_template('add_note.html', form=form)

@bp.route('/note/<int:note_id>/attachments/', methods=['GET', 'POST'])
@login_required
def get_attachments(note_id):
    attachements = get_db().get_attachements_by_note_id(note_id)
    
    secure_temp = tempfile.TemporaryDirectory(dir=current_app.config['ATTACHEMENTS'])
    for attachement in attachements:
        os.system(f'cp {attachement} {secure_temp.name}')
    shutil.make_archive(base_name=os.path.join(secure_temp.name, 'attachements.zip')[:-4], format='zip', root_dir=secure_temp.name)
    
    return send_file(os.path.join(secure_temp.name, 'attachements.zip'),
                    as_attachment=True)