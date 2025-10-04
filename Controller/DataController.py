import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Model', 'Query'))

from DB import db # type: ignore
from Model.Query import select

database = db()

def load_data(table_name):
    try:
        if table_name == 'courses':
            relation = [['doctors', 'doctor_id = doctors.id']]
            cursor = select.select(database, table_name, relation, "courses.id AS id", "name", "doctors.first_name || ' ' || doctors.last_name AS doctor_name", "price", "start_date", "end_date")
        else:
            cursor = select.select(database, table_name)
    except Exception as error:
        print(f"Failed loading data: {error}")
        return None
    rows = cursor.fetchall()
    return rows

def is_student_enrolled_to(sID, course_name):
    query = """
        SELECT 1 FROM student_course
        WHERE student_id = ? AND course_name = ?
        LIMIT 1
    """
    cursor = database.cursor()
    cursor.execute(query, (sID, course_name))
    result = cursor.fetchone()
    return result is not None

def enroll_student_to_course(sID, course_name):
    # Get course info
    cursor = database.cursor()
    cursor.execute("""
        SELECT id, doctor_id, price, start_date, end_date
        FROM courses
        WHERE name = ?
        LIMIT 1
    """, (course_name,))
    course = cursor.fetchone()

    if not course:
        print(f"Course '{course_name}' not found.")
        return False

    course_id, doctor_id, course_price, course_start_date, course_end_date = course

    # Insert into student_course
    cursor.execute("""
        INSERT INTO student_course (
            student_id, doctor_id, course_name, course_price,
            course_start_date, course_end_date, enrollment_date, course_id
        ) VALUES (?, ?, ?, ?, ?, ?, DATE('now'), ?)
    """, (
        sID, doctor_id, course_name, course_price,
        course_start_date, course_end_date, course_id
    ))
    database.commit()
    return True

def add_new_apyment(sID, course_name, paid, pay_type, date):
    cursor = database.cursor()
    # Get the student_course id for this student and course
    cursor.execute("""
        SELECT id FROM student_course
        WHERE student_id = ? AND course_name = ?
        ORDER BY id DESC LIMIT 1
    """, (sID, course_name))
    result = cursor.fetchone()
    if not result:
        print("Student is not enrolled in this course.")
        return False
    student_course_id = result[0]

    # Insert the payment
    cursor.execute("""
        INSERT INTO payments (student_id, student_course_id, payment_date, payment_type, amount_paid)
        VALUES (?, ?, ?, ?, ?)
    """, (sID, student_course_id, date, pay_type, paid))
    database.commit()
    return True

def confirm_payment(sID, course_name, paid, pay_type, date):
    # check if is already enrolled
    if not is_student_enrolled_to(sID, course_name):
        # enroll student to course
        if enroll_student_to_course(sID, course_name):
            print("enrolled successfully!")
        else:
            print("error enrolling student to course!")
            return

    # pay amount to student_course table
    add_new_apyment(sID, course_name, paid, pay_type, date)

def add_new_student(fname, lname, gender, country, phone, address=None, email=None, university=None, barcode=None):
    cursor = database.cursor()
    try:
        cursor.execute("""
            INSERT INTO students (first_name, last_name, gender, country_code, phone_number, address, email, university, barcode)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (fname, lname, gender, country, phone, address, email, university, barcode))
        database.commit()
        return True
    except Exception as error:
        print(f"Failed creating new student: {error}")
        return False

    
def get_full_name(fname, lname):
    return fname + " " + lname

def get_doctors_names_id():
    doctors = select.select_doctors(database, "id", "first_name", "last_name").fetchall()
    names = []
    ids = []
    for rec in doctors:
        names.append(get_full_name(rec[1], rec[2]))
        ids.append(rec[0])

    return names,ids