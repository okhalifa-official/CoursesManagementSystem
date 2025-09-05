-- Create Main Entities --

CREATE TABLE students
(
    id INT NOT NULL UNIQUE,
    name VARCHAR2(50)
);

CREATE TABLE student_enrollment
(
    id INT NOT NULL UNIQUE,
    student_id INT,
    course_id INT
);

CREATE TABLE courses
(
    id INT NOT NULL UNIQUE,
    name VARCHAR2(20),
    doctor_id INT
);

CREATE TABLE payments
(
    id INT NOT NULL UNIQUE,
    student_id INT,
    course_id INT
);

CREATE TABLE doctors
(
    id INT NOT NULL UNIQUE,
    name VARCHAR2(50)
);

-- Add Relations --

ALTER TABLE student_enrollment
ADD CONSTRAINT fk_student_id
FOREIGN KEY (student_id) REFERENCES students(id)
ON DELETE CASCADE;

ALTER TABLE student_enrollment
ADD CONSTRAINT fk_course_id
FOREIGN KEY (course_id) REFERENCES courses(id)
ON DELETE CASCADE;

ALTER TABLE payments
ADD CONSTRAINT fk_payment_student_id
FOREIGN KEY (student_id) REFERENCES students(id)
ON DELETE CASCADE;

ALTER TABLE payments
ADD CONSTRAINT fk_payment_course_id
FOREIGN KEY (course_id) REFERENCES courses(id)
ON DELETE CASCADE;

ALTER TABLE courses
ADD CONSTRAINT fk_courses_doctor_id
FOREIGN KEY (doctor_id) REFERENCES doctors(id)
ON DELETE CASCADE;

ALTER TABLE student_enrollment
ADD CONSTRAINT pk_student_enrollment
PRIMARY KEY (student_id, course_id);