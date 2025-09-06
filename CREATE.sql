CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE doctors (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    name TEXT,
    doctor_id INTEGER,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
);

CREATE TABLE student_enrollment (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE (student_id, course_id)
);

CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);