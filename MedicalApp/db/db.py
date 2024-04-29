import oracledb
import os
from flask import g
from ..appointments import Appointments
from ..user import MedicalPatient
from ..note import Note
from werkzeug.security import generate_password_hash

from MedicalApp.user import User
from MedicalApp.appointments import Appointments


class Database:
    def __init__(self, autocommit=True):
        self.__connection = oracledb.connect(user=os.environ['DBUSER'], password=os.environ['DBPWD'],
                                             host="198.168.52.211", port=1521, service_name="pdbora19c.dawsoncollege.qc.ca")
        self.__connection.autocommit = autocommit

    def run_file(self, file_path):
        statement_parts = []
        with self.__connection.cursor() as cursor:
            with open(file_path, 'r') as f:
                for line in f:
                    statement_parts.append(line)
                    if line.strip('\n').strip('\n\r').strip().endswith(';'):
                        statement = "".join(
                            statement_parts).strip().rstrip(';')
                        if statement:
                            try:
                                cursor.execute(statement)
                            except Exception as e:
                                print(e)
                        statement_parts = []
        
    def delete_user(self, user_email):
        try:
            with self.__connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM medical_users WHERE email = :email",
                    {'email': user_email}
                )
                self.__connection.commit()
        except Exception as e:
            print("Error deleting user:", e)
            raise
        
    def block_user(self, email):
        try:
            with self.__connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE medical_users SET account_status = 'blocked' WHERE email = :email",
                    {'email': email}
                )
                self.__connection.commit()
        except Exception as e:
            print("Error blocking user:", e)
            raise
        
    def change_user_type(self, user_email, new_user_type):
        try:
            with self.__connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE medical_users SET user_type = :user_type WHERE email = :email",
                    {'user_type': new_user_type, 'email': user_email}
                )
                self.__connection.commit()
        except Exception as e:
            print("Error changing user type:", e)
            raise
    
    
    # status 0 = pending, status 1 = confirmed, status -1 = cancel
    def get_appointments_by_status(self, status, doctor_id):
        appointments = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT id, patient_id, doctor_id, appointment_time, status, location, description FROM medical_appointments WHERE status = :status AND doctor_id = :doctor_id",
                status=status, doctor_id=doctor_id)
            for row in results:
                appointments.append(Appointments(int(row[0]), int(row[1]), int(
                    row[2]), str(row[3]), int(row[4]), row[5], str(row[6])))
        return appointments

    def get_appointment_by_id(self, id):
        appointment = None
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT id, patient_id, doctor_id, appointment_time, status, location, description FROM medical_appointments WHERE id = :id",
                id=id)
            row = results.fetchone()
            if row:
                appointment = Appointments(int(row[0]), int(row[1]), int(
                    row[2]), str(row[3]), int(row[4]), row[5], str(row[6]))
        return appointment
    
    def get_appointment_for_doctors(self):
        appointment = None
        with self.__get_cursor() as cursor:
            cursor.execute(
                'SELECT app.id, app.patient_id, app.doctor_id, app.appointment_time, app.status, app.location, app.description,d.ID, d.AVATAR_PATH, d.EMAIL, d.FIRST_NAME, d.LAST_NAME, d.PASSWORD, d.USER_TYPE,p.id, p.AVATAR_PATH, p.EMAIL, p.PASSWORD, p.FIRST_NAME, p.LAST_NAME, p.USER_TYPE,mp.BLOOD_TYPE, mp.DOB, mp.HEIGHT, mp.WEIGHT FROM medical_appointments app INNER JOIN medical_users d ON app.doctor_id = d.id INNER JOIN medical_users p ON app.PATIENT_ID = p.ID INNER JOIN MEDICAL_PATIENTS mp ON mp.id = p.id WHERE d.id = :doctor_id')
            row = cursor.fetchone()
            if row:
                appointment = Appointments(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return appointment
    
    
    def get_appointment_for_patients(self):
        appointment = None
        with self.__get_cursor() as cursor:
            cursor.execute(
                'SELECT app.id, app.patient_id, app.doctor_id, app.appointment_time, app.status, app.location, app.description,d.ID, d.AVATAR_PATH, d.EMAIL, d.FIRST_NAME, d.LAST_NAME, d.PASSWORD, d.USER_TYPE,p.id, p.AVATAR_PATH, p.EMAIL, p.PASSWORD, p.FIRST_NAME, p.LAST_NAME, p.USER_TYPE,mp.BLOOD_TYPE, mp.DOB, mp.HEIGHT, mp.WEIGHT FROM medical_appointments app INNER JOIN medical_users d ON app.doctor_id = d.id INNER JOIN medical_users p ON app.PATIENT_ID = p.ID INNER JOIN MEDICAL_PATIENTS mp ON mp.id = p.id WHERE p.id = :patient_id')
            row = cursor.fetchone()
            if row:
                appointment = Appointments(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return appointment

    def get_user_by_id(self, id):
        patient = None
        with self.__get_cursor() as cursor:
            results = cursor.execute("SELECT email, password, first_name, last_name, user_type, avatar_path, id FROM medical_users WHERE id = :id",
                                     id=id)
            row = results.fetchone()
            if row:
                patient = User(
                    row[0], row[1], row[2], row[3], row[4], avatar_path=row[5], id=int(row[6]))
        return (patient)

    def update_appointment_status(self, id, status):
        with self.__get_cursor() as cursor:
            cursor.execute("UPDATE medical_appointments SET status = :status WHERE id = :id",
                           status=status, id=id)

    def get_patients_by_doctor(self, doctor_id):
        patients = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT weight, email, password, first_name, last_name, user_type, dob, blood_type, height, avatar_path, users.id FROM medical_users users INNER JOIN medical_patients p ON(users.id = p.id) INNER JOIN medical_appointments appts ON(users.id = appts.patient_id) WHERE doctor_id = :id",
                id=doctor_id)
            for row in results:
                patients.append(MedicalPatient(
                    float(row[0]), row[1], row[2], row[3], row[4], str(row[5]), str(row[6]), str(row[7]), float(row[8]), avatar_path= str(row[9]), id=int(row[10])))
        return patients

    def get_patients_by_id(self, patient_id):
        patient = None
        with self.__get_cursor() as cursor:
            results = cursor.execute("SELECT weight, email, password, first_name, last_name, user_type, dob, blood_type, height, avatar_path, id FROM medical_users u INNER JOIN medical_patients p USING(id) WHERE id = :id",
                                     id=patient_id)
            row = results.fetchone()
            if row:
                patient = MedicalPatient(float(row[0]), row[1], row[2], row[3], row[4], str(row[5]), str(row[6]), str(row[7]), float(row[8]), avatar_path=row[9], id=int(row[10]))
        return patient

    def get_notes_by_patient_id(self, patient_id):
        notes = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT n.id, n.note_date, n.note, p.weight, p.email, p.password, p.first_name, p.last_name, p.user_type, p.dob, p.blood_type, p.height, p.avatar_path, p.id, d.email, d.password, d.first_name, d.last_name, d.user_type, d.avatar_path, d.id, a.attachement_path FROM medical_notes n INNER JOIN medical_patients p ON (n.patient_id = p.id) INNER JOIN medical_users u ON(d.id = n.note_taker_id) INNER JOIN medical_note_attachements a ON(a.note_id = n.id) WHERE patient_id = :patient_id",
                patient_id=patient_id)
            for row in results:
                doctor = User(
                    row[14], row[15], row[16], row[17], row[18], avatar_path=row[19], id=int(row[20]))
                patient = MedicalPatient(float(row[3]), row[4], row[5], row[6], row[7], str(row[8]), str(row[9]), str(row[10]), float(row[11]), avatar_path=row[12], id=int(row[13]))
                notes.append(Note(
                    int(row[0]), patient, doctor, str(row[1]), str(row[2]), str(row[21])))
        return notes
    
    def get_notes_by_doctor_id(self, doctor_id):
        notes = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                """
                SELECT n.id, n.note_date, n.note, p.weight, up.email, up.password, up.first_name, up.last_name, up.user_type, p.dob, p.blood_type, p.height, up.avatar_path, p.id, d.email, d.password, d.first_name, d.last_name, d.user_type, d.avatar_path, d.id, a.attachment_path
                FROM medical_notes n INNER JOIN medical_users up
                    ON (n.patient_id = up.id) INNER JOIN medical_patients p
                    ON (up.id = p.id)
                    INNER JOIN medical_users d ON(d.id = n.note_taker_id)
                    INNER JOIN medical_note_attachments a ON(a.note_id = n.id)
                WHERE note_taker_id = :doctor_id
                """,
                doctor_id=doctor_id)
            for row in results:
                doctor = User(
                    row[14], row[15], row[16], row[17], row[18], avatar_path=row[19], id=int(row[20]))
                patient = MedicalPatient(float(row[3]), row[4], row[5], row[6], row[7], str(row[8]), str(row[9]), str(row[10]), float(row[11]), avatar_path=row[12], id=int(row[13]))
                notes.append(Note(
                    patient, doctor, row[1], str(row[2]), attachement_path=str(row[21]), id=int(row[0])))
        return notes
    
    def create_note(self, note):
        if not isinstance(note, Note):
            raise TypeError("expected Note object")
        with self.__get_cursor() as cursor:
            new_id = cursor.var(oracledb.NUMBER)
            cursor.execute('insert into medical_notes (patient_id, note_taker_id, note_date, note)  values (:patient_id, :note_taker_id, :note_date, :note) returning id into :id',
                           patient_id=note.patient.id,
                           note_taker_id=note.note_taker.id,
                           note_date=note.note_date,
                           note=note.note,
                           id=new_id)
            cursor.execute('insert into medical_note_attachments (note_id, attachment_path)  values (:note_id, :attachement_path)',
                           note_id=int(new_id.values[0][0]),
                           attachement_path=str(note.attachement_path))


    def create_user(self, user):
        if not isinstance(user, User):
            raise TypeError("expected User object")
        with self.__get_cursor() as cursor:
            cursor.execute('insert into medical_users (email, password, first_name,last_name,user_type)  values (:email, :password, :first_name, :last_name, :user_type)',
                           email=user.email,
                           password=user.password,
                           first_name=user.first_name,
                           last_name=user.last_name,
                           user_type=user.access_level)

    def get_user_by_email(self, email):
        user = None
        with self.__get_cursor() as cursor:
            cursor.execute(
                'select email, password, first_name, last_name, user_type, avatar_path, id from medical_users where email=:email', email=email)
            row = cursor.fetchone()
            if row:
                user = User(
                    row[0], row[1], row[2], row[3], row[4], avatar_path=row[5], id=int(row[6]))
        return user

    def add_appointment(self, appointment):
        with self.__get_cursor() as cursor:
            if not isinstance(appointment, Appointments):
                raise TypeError("expected Appointment object")
            with self.__get_cursor() as cursor:
                cursor.execute('insert into medical_appointments (id, patient_id, doctor_id, appointment_time, status, location, description) values (:id, :patient_id, :doctor_id, :appointment_time, :status, :location, :description)',
                               id=appointment.id,
                               patient_id=appointment.patients.id,
                               doctor_id=appointment.doctors.id,
                               appointment_time=appointment.appointment_time,
                               status=appointment.status,
                               location=appointment.location,
                               description=appointment.description)

    def delete_appointment_by_id(self, id):
        with self.__get_cursor() as cursor:
            if not isinstance(id, int):
                raise TypeError("expected type of integer")
            with self.__get_cursor() as cursor:
                    cursor.execute("DELETE FROM medical_appointments WHERE id = :id", id=id)


    def update_appointment(self,appointment):
        with self.__get_cursor() as cursor:
            if not isinstance(appointment, Appointments):
                raise TypeError("expected type of Appointmentsr")
            with self.__get_cursor() as cursor:
                    cursor.execute(" UPDATE medical_appointments SET patient_id =: patient_id, doctor_id =: doctor_id, appointment_time =: appointment_time, status =: status, location =: location, description =: description WHERE id =:id", patient_id=appointment.patients.id, doctor_id=appointment.doctors.id, appointment_time=appointment.appointment_time, status=appointment.status, location=appointment.location, description=appointment.description, id=appointment.id)

    def get_appointments(self):
        appointments = []
        with self.__get_cursor() as cursor:
            results = cursor.execute('SELECT app.id, app.patient_id, app.doctor_id, app.appointment_time, app.status, app.location, app.description, p.dob, p.blood_type, p.height, p.weight, mu1.email as patient_email, mu1.first_name as patient_first_name, mu1.last_name as patient_last_name, mu2.email as doctor_email, mu2.first_name as doctor_first_name, mu2.last_name as doctor_last_name FROM medical_appointments app INNER JOIN medical_users mu1 ON app.patient_id = mu1.id INNER JOIN medical_users mu2 ON app.doctor_id = mu2.id INNER JOIN medical_patients p ON app.patient_id = p.id')
            for row in results:
                patient = MedicalPatient(
                    row[10], row[11], row[12], row[13], row[14], 'PATIENT', row[7], row[8], row[9], row[10])  
                doctor = User(row[15], None, row[16], row[17])  
                appointment = Appointments(
                    row[0], patient, doctor, row[3], row[4], row[5], row[6])
                appointments.append(appointment)
        return appointments


    def __get_cursor(self):
        for i in range(3):
            try:
                return self.__connection.cursor()
            except Exception as e:
                # Might need to reconnect
                self.__reconnect()

    def __reconnect(self):
        try:
            self.close()
        except oracledb.Error as f:
            pass
        self.__connection = self.__connect()

    def __connect(self):
        return oracledb.connect(user=os.environ['DBUSER'], password=os.environ['DBPWD'],
                                host="198.168.52.211", port=1521, service_name="pdbora19c.dawsoncollege.qc.ca")

    def close(self):
        '''Closes the connection'''
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None


if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')
