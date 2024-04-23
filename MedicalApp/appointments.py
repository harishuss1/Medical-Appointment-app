import json
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired


class Appointments:
    def from_json(data):
        if not isinstance(data, dict):
            raise TypeError()
        return Appointments(data['id'], data['patient_id'], data['doctor_id'], data['appointment_time'],
                            data['status'], data['location'], data['description'])

    def to_json(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'appointment_time': self.appointment_time,
            'status': self.status,
            'location': self.location,
            'description': self.description
        }

    def __init__(self, id, patient_id, doctor_id, appointment_time, status, location, description):
        if not isinstance(id, int) or id < 0:
            raise ValueError('Illegal type for patient id')
        self.id = id

        if not isinstance(patient_id, int) or patient_id < 0:
            raise ValueError('Illegal type for patient id')
        self.patient_id = patient_id

        if not isinstance(doctor_id, int) or doctor_id < 0:
            raise ValueError(
                'Id must be positive or Illegal type for doctor id')
        self.doctor_id = doctor_id

        if not isinstance(appointment_time, str):
            raise ValueError('Illegal type for appointment_time')
        self.appointment_time = appointment_time

        if not isinstance(status, int or status > 1 or status < -1):
            raise ValueError('Illegal type for status')
        self.status = status

        if not isinstance(location, str):
            raise ValueError('Illegal type for location')
        self.location = location

        if not isinstance(description, str):
            raise ValueError('Illegal type for description')
        self.description = description

    def __str__(self):
        return f'{self.id} {self.patient_id} {self.doctor_id} {self.appointment_time} {self.status} {self.location} {self.description}'
