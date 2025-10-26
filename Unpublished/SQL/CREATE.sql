CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender VARCHAR(8),
    country_code VARCHAR(5) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    address TEXT NULL,
    email TEXT NULL,
    university TEXT NOT NULL,
    barcode VARCHAR(20) NULL
);

CREATE TABLE doctors (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender VARCHAR(8),
    email TEXT NULL,
    country_code VARCHAR(5) NOT NULL,
    phone_number VARCHAR(15) NOT NULL
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    doctor_id INTEGER,
    price INTEGER NOT NULL,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE SET NULL
);

CREATE TABLE student_course (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    doctor_id INTEGER,
    course_name TEXT,         
    course_price INTEGER,     
    course_start_date DATE,   
    course_end_date DATE,
    enrollment_date DATE,
    course_id INTEGER,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE SET NULL,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE SET NULL,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE SET NULL
);

CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    student_course_id INTEGER,
    payment_date DATE,
    payment_type TEXT,
    amount_paid INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (student_course_id) REFERENCES student_course(id) ON DELETE CASCADE
);

CREATE TABLE withdraws(
    id INTEGER PRIMARY KEY,
    doctor_id INTEGER,
    withdraw_date DATE,
    withdraw_type TEXT,
    amount INTEGER
);
