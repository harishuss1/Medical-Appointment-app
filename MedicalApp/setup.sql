--calling table drops
@remove.sql

@users.sql

create table medical_patients(
    id  INTEGER not null,  
    dob date not null,
    blood_type varchar(3),
    height float,
    weight float,
    CONSTRAINT p_fk FOREIGN KEY (id) REFERENCES medical_users(id)
);

create table medical_allergies (
    id           INTEGER
        GENERATED BY DEFAULT ON NULL AS IDENTITY primary key,
    name varchar2(1000) not null,
    description varchar2(2000) not null
);

create table medical_patient_allergies(
    patient_id integer,
    allergy_id integer,
    CONSTRAINT pa_fk FOREIGN KEY (patient_id) REFERENCES medical_users(id),
    CONSTRAINT a_fk FOREIGN KEY (allergy_id) REFERENCES medical_allergies(id)
);

create table medical_rooms(
    room_number varchar2(20) primary key,    
    description varchar2(200)
);

/*
* status has 3 values, 0 meaning Pending, 1 meaning accepted, -1 meaning denied
*/
create table medical_appointments(
    id           INTEGER
        GENERATED BY DEFAULT ON NULL AS IDENTITY primary key,
    patient_id integer,
    doctor_id integer,
    appointment_time timestamp,
    status integer not null,
    location varchar2(20),
    description nclob,
    CONSTRAINT status_value CHECK (status = 0 OR status = -1 or status = 1),
    CONSTRAINT location_fk FOREIGN KEY (location) REFERENCES medical_rooms(room_number),
    CONSTRAINT pid_fk FOREIGN KEY (patient_id) REFERENCES medical_users(id),
    CONSTRAINT did_fk FOREIGN KEY (doctor_id) REFERENCES medical_users(id)
);

create table medical_notes(
    id           INTEGER
        GENERATED BY DEFAULT ON NULL
    as identity PRIMARY KEY,
    patient_id INTEGER,
    note_taker_id INTEGER,
    note_date TIMESTAMP NOT NULL,
    note NCLOB,
    constraint pan_fk FOREIGN KEY(patient_id)
        REFERENCES medical_users(id),
    constraint n_fk FOREIGN KEY(note_taker_id)
        REFERENCES medical_users(id)
);

create table medical_note_attachments(
    note_id integer,
    attachment_path varchar2(1000) not null,
    CONSTRAINT note_fk FOREIGN KEY (note_id) REFERENCES medical_notes(id)
);

commit;