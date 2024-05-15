import datetime

import oracledb
from MedicalApp.allergy import Allergy
from ..user import User, MedicalPatient
from oracledb import IntegrityError
from ..appointments import Appointments


class FakeDB:

    def __init__(self):
        self.allergies = [Allergy(1, "Peanuts", "Allergic reaction to peanuts causing hives and swelling."), Allergy(
            2, "Penicillin", "Allergic reaction to penicillin causing difficulty breathing and rash.")]
        self.tokens = ["km9b5-UeGr3SDy6PszxFZRRvqiE",
                       "mIzbZLyEzNKW7SP5NAx9eUHUq_w", "tF1fG-t-R5hu3USXZcDIlKvIwXI", "ErU49l4Du_LEvsV1AgU9SIllZ1g", "2z12xfm3gqvZr1kZIAi4YXahpeA"]
        self.patients = []
        #                                  weight, email,              password,                                                                                                                                                            first_name, last_name, access_level, dob,              blood_type, height, allergies=None, avatar_path=None, id=None
        self.patients.append(MedicalPatient(68.0, "maddie@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68",
                             "Maddie", "Buckley", "PATIENT", datetime.date(1985, 10, 5), "O-", 168.0, allergies=[self.allergies[0]], id=6, tokens=[self.tokens[0]]))
        self.patients.append(MedicalPatient(70.2, "chimney@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68",
                             "Howard", "Han", "PATIENT", datetime.date(1985, 10, 5), "A+", 168.0, id=7, tokens=[self.tokens[1]]))
        self.patients.append(MedicalPatient(75.2, "eddie@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68",
                             "Eddie", "Diaz", "PATIENT", datetime.date(1985, 10, 5), "B+", 170.0, id=8, tokens=[self.tokens[2]]))
        self.users = []
        self.users.append(User("maddie@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68", "Maddie", "Buckley", "PATIENT", tokens=[self.tokens[0]], id=6))
        self.users.append(User("chimney@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68", "Howard", "Han", "PATIENT", tokens=[self.tokens[1]], id=7))
        self.users.append(User("eddie@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68", "Eddie", "Diaz", "PATIENT", tokens=[self.tokens[2]], id=8))
        self.users.append(User("bobby@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68", "Bobby", "Nash", "DOCTOR", tokens=[self.tokens[3]], id=9))
        self.users.append(User("blocked@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68", "Blocked", "User", "BLOCKED", tokens=[self.tokens[3]], id=10))
        self.appointments = []

    def get_user_by_token(self, token):
        if (not isinstance(token, str)):
            raise TypeError("Parameters of incorrect type")

        for user in self.users:
            if (token in user.tokens):
                return user
        return None

    def get_appointment_by_id(self, appointment_id):
        if (appointment_id is None):
            raise ValueError("Parameters cannot be None")
        try:
            appointment_id = int(appointment_id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        for appointment in self.appointments:
            if appointment.id == appointment_id:
                return appointment
        return None

    def get_appointments(self):
        return self.appointments

    def add_appointment(self, appointment):
        if not isinstance(appointment, Appointments):
            raise TypeError("Invalid appointment type")
        self.appointments.append(appointment)

    def get_all_allergies(self):
        return self.allergies

    def get_patients(self):
        return self.patients

    def get_patient_allergies(self, patient_id):
        if (patient_id is None):
            raise ValueError("Parameters cannot be none")
        try:
            patient_id = int(patient_id)
        except:
            raise TypeError("Parameters of incorrect type")

        patient = self.get_patients_by_id(patient_id)
        return patient.allergies
    
    def get_allergy_by_id(self, id):
        if (id is None):
            raise ValueError("Parameters cannot be None")
        try:
            id = int(id)
        except:
            raise TypeError("Parameters of incorrect type")
        allergy = None
        for a in self.allergies:
            if a.id == id:
                allergy = a
        return allergy
    
    def update_allergies(self, patient_id, allergy_ids):
        if (patient_id is None or allergy_ids is None):
            raise ValueError("Parameters cannot be none")
        try:
            patient_id = int(patient_id)
            for allergy in allergy_ids:
                int(allergy)
        except:
            raise TypeError("Parameters of incorrect type")
        
        new_allergies = []
        
        for id in allergy_ids:
            allergy = self.get_allergy_by_id(id)
            if allergy is None:
                raise oracledb.IntegrityError()
            new_allergies.append(allergy)
        
        patient = self.get_patients_by_id(patient_id)
        patient.allergies = new_allergies

    def get_patients_page_number(self, page, first_name, last_name):
        if (page is None):
            raise ValueError("Parameters cannot be none")
        if (first_name is not None and not isinstance(first_name, str) or last_name is not None and not isinstance(last_name, str)):
            raise TypeError("Parameters of incorrect type")

        try:
            page = int(page)
        except:
            raise TypeError("Parameters of incorrect type")

        patients = []
        offset = ((page - 1)*2)
        count = 2
        
        end = count+offset if count+offset <= len(self.patients) else len(self.patients)

        for i in range(offset, end):
            patient = self.patients[i]
            if first_name is None and last_name is None:
                patients.append(patient)
            if first_name is not None and patient.first_name == first_name:
                patients.append(patient)
            if last_name is not None and patient.last_name == last_name:
                patients.append(patient)
        return patients

    def get_patients_by_id(self, patient_id):
        if (patient_id is None):
            raise ValueError("Parameters cannot be none")
        try:
            patient_id = int(patient_id)
        except:
            raise TypeError("Parameters of incorrect type")

        patient = None
        for p in self.patients:
            if p.id == patient_id:
                patient = p
        return patient

    def run_file(self, file_path):
        pass

    def close(self):
        pass
