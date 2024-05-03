INSERT INTO medical_access_level (user_type) VALUES ('BLOCKED');
INSERT INTO medical_access_level (user_type) VALUES ('PATIENT');
INSERT INTO medical_access_level (user_type) VALUES ('STAFF');
INSERT INTO medical_access_level (user_type) VALUES ('ADMIN');
INSERT INTO medical_access_level (user_type) VALUES ('ADMIN_USER');

INSERT INTO medical_users (email, password, first_name, last_name, avatar_path, user_type)
VALUES ('patient1@example.com', 'scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68', 'Evan', 'Buckley', '/avatars/evan_buckley.jpg', 'PATIENT');

INSERT INTO medical_users (email, password, first_name, last_name, avatar_path, user_type)
VALUES ('doctor@example.com', 'scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68', 'Howey', 'Han', '/avatars/dr_han.jpg', 'STAFF');

INSERT INTO medical_users (email, password, first_name, last_name, avatar_path, user_type)
VALUES ('admin@example.com', 'scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68', 'Admin', 'Adminson', '/avatars/admin.jpg', 'ADMIN');

INSERT INTO medical_patients (id, dob, blood_type, height, weight)
VALUES (1, '1990-05-15', 'A+', 175.5, 70.3);

INSERT INTO medical_patients (id, dob, blood_type, height, weight)
VALUES (2, '1985-08-20', 'AB-', 162.0, 65.8);

INSERT INTO medical_allergies (name, description)
VALUES ('Peanuts', 'Allergic reaction to peanuts causing hives and swelling.');

INSERT INTO medical_allergies (name, description)
VALUES ('Penicillin', 'Allergic reaction to penicillin causing difficulty breathing and rash.');

INSERT INTO medical_patient_allergies (patient_id, allergy_id)
VALUES (1, 1);

INSERT INTO medical_patient_allergies (patient_id, allergy_id)
VALUES (2, 2);

INSERT INTO medical_rooms (room_number, description) VALUES ('101', 'Emergency Room');
INSERT INTO medical_rooms (room_number, description) VALUES ('102', 'Operating Room 1');
INSERT INTO medical_rooms (room_number, description) VALUES ('103', 'Operating Room 2');
INSERT INTO medical_rooms (room_number, description) VALUES ('104', 'Intensive Care Unit (ICU)');
INSERT INTO medical_rooms (room_number, description) VALUES ('105', 'Labor and Delivery Room');
INSERT INTO medical_rooms (room_number, description) VALUES ('106', 'Neonatal Intensive Care Unit (NICU)');
INSERT INTO medical_rooms (room_number, description) VALUES ('107', 'Radiology Department');
INSERT INTO medical_rooms (room_number, description) VALUES ('108', 'Pharmacy');
INSERT INTO medical_rooms (room_number, description) VALUES ('109', 'Physical Therapy Room');
INSERT INTO medical_rooms (room_number, description) VALUES ('110', 'Cardiac Catheterization Lab');
INSERT INTO medical_rooms (room_number, description) VALUES ('111', 'Endoscopy Suite');
INSERT INTO medical_rooms (room_number, description) VALUES ('112', 'Ultrasound Room');
INSERT INTO medical_rooms (room_number, description) VALUES ('113', 'MRI Room');
INSERT INTO medical_rooms (room_number, description) VALUES ('114', 'CT Scan Room');
INSERT INTO medical_rooms (room_number, description) VALUES ('115', 'Nuclear Medicine Room');
INSERT INTO medical_rooms (room_number, description) VALUES ('116', 'Mammography Room');
INSERT INTO medical_rooms (room_number, description) VALUES ('117', 'Recovery Room');
INSERT INTO medical_rooms (room_number, description) VALUES ('118', 'Patient Ward 1');
INSERT INTO medical_rooms (room_number, description) VALUES ('119', 'Patient Ward 2');
INSERT INTO medical_rooms (room_number, description) VALUES ('120', 'Pediatric Ward');


INSERT INTO medical_appointments (patient_id, doctor_id, appointment_time, status, location, description)
VALUES (1, 2, '2024-04-24 10:00:00', 0, '101', 'Routine checkup.');

INSERT INTO medical_appointments (patient_id, doctor_id, appointment_time, status, location, description)
VALUES (2, 2, '2024-04-25 11:30:00', 1, '102', 'Follow-up appointment.');

INSERT INTO medical_notes (patient_id, note_taker_id, note_date, note)
VALUES (1, 2, '2024-04-24 09:30:00', 'Patient presented with symptoms of flu. Prescribed medication and advised bed rest.');

INSERT INTO medical_notes (patient_id, note_taker_id, note_date, note)
VALUES (2, 2, '2024-04-25 12:00:00', 'Follow-up examination conducted. Patient reports improvement in condition. Continuing current medication.');

INSERT INTO medical_note_attachments (note_id, attachment_path)
VALUES (1, '/attachments/note1_attachment.pdf');

INSERT INTO medical_note_attachments (note_id, attachment_path)
VALUES (2, '/attachments/note2_attachment.jpg');

INSERT INTO medical_api_tokens (user_id, token)
VALUES (1, 'e5a9b9c4f34597ae9b9c4e5a9b9c4f34597ae9b9c4e5a9b9');

INSERT INTO medical_api_tokens (user_id, token)
VALUES (2, 'b9c4e5a9b9c4f34597ae9b9c4e5a9b9c4f34597ae9b9c4e5a9');

COMMIT;