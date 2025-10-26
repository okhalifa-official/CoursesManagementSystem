import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Model', 'Query'))
import tkinter as tk
from tkinter import ttk, messagebox
from Controller.Validation import Validation
from Controller import PopupHandler
from DB import db # type: ignore
from Model.Query import select, delete

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

def load_data_with_args(From, Where, Value, Columns=["*"], Operations=[], group=[], Order=[]):
    columns_string = ""
    from_string = ""
    condition_string = ""
    group_string = ""
    order_string = ""
    for i,col in enumerate(Columns):
        columns_string += col
        if i < len(Columns)-1:
            columns_string += ', '
    for i,Frm in enumerate(From):
        from_string += Frm
        if i < len(From)-1:
            from_string += ', '
    for i in range(min(len(Where), len(Value))):
        operation = '='
        if i < len(Operations):
            operation = Operations[i]
        condition_string += Where[i] + operation + str(Value[i])
        if i < min(len(Where), len(Value))-1:
            condition_string += ' AND '
    for i,grp in enumerate(group):
        group_string += grp
        if i < len(group)-1:
            group_string += ', '
    for i,ordr in enumerate(Order):
        order_string += ordr
        if i < len(Order)-1:
            order_string += ', '

    result = select.select_with_args(database=database,columns=columns_string, froms=from_string, conditions=condition_string, group=group_string, order=order_string)
    if result is None:
        print('Error fetching result')
        return None
    return result

def is_student_enrolled_to(sID, course_name):
    # Ask for the id column; check truthiness of result (non-empty list == enrolled)
    result = load_data_with_args(
        From=['student_course'],
        Where=['student_id', 'course_name'],
        Columns=['id'],
        Value=[sID, f'"{course_name}"']
    )
    return bool(result)  # True if list contains at least one row

def enroll_student_to_course(sID, course_name):
    # Get course info
    course = load_data_with_args(
        From=['courses'],
        Where=['name'],
        Columns=['id', 'doctor_id', 'price', 'start_date', 'end_date'],
        Value=[f'"{course_name}"']
    )

    if course is None or len(course) == 0:
        print(f"Course '{course_name}' not found.")
        return False

    course_id, doctor_id, course_price, course_start_date, course_end_date = course[0]

    # Insert into student_course
    cursor = database.cursor()
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


def add_new_payment(sID, course_name, paid, pay_type, date):
    # Get the student_course id for this student and course
    result = load_data_with_args(
        From=['student_course'],
        Where=['student_id', 'course_name'],
        Columns=['id'],
        Value=[sID, f'"{course_name}"']
    )

    # ⚠️ Check if result is empty or None
    if not result or len(result) == 0:
        print("Student is not enrolled in this course.")
        return False

    student_course_id = result[0][0]

    # Insert the payment
    cursor = database.cursor()
    cursor.execute("""
        INSERT INTO payments (student_id, student_course_id, payment_date, payment_type, amount_paid)
        VALUES (?, ?, ?, ?, ?)
    """, (sID, student_course_id, date, pay_type, paid))
    
    database.commit()
    return True


def confirm_payment(pID, sID, course_name, paid, pay_type, date):
    # check if student is already enrolled
    if not is_student_enrolled_to(sID, course_name):
        # try to enroll student
        enrolled = enroll_student_to_course(sID, course_name)
        if not enrolled:
            print("Error: could not enroll student to course. Payment aborted.")
            return False
        print("Enrolled successfully!")

    # Now add the payment
    paid_ok = add_new_payment(sID, course_name, paid, pay_type, date)
    if not paid_ok:
        print("Error: failed to record payment.")
        return False

    print("Payment confirmed.")
    return True

def update_payment(pID, sID, course_name, paid, pay_type, date):
    cursor = database.cursor()

    # Get the student_course id for this student and course
    result = load_data_with_args(
        From=['student_course'],
        Where=['student_id', 'course_name'],
        Columns=['id'],
        Value=[sID, f'"{course_name}"'],
        Order=['id']
    )

    if not result:
        print("Student is not enrolled in this course.")
        return False

    student_course_id = result[0][0]

    try:
        cursor.execute("""
            UPDATE payments
            SET student_id = ?, student_course_id = ?, payment_date = ?, payment_type = ?, amount_paid = ?
            WHERE id = ?
        """, (sID, student_course_id, date, pay_type, paid, pID))

        if cursor.rowcount == 0:
            print(f"No payment found with ID {pID}.")
            return False

        database.commit()
        print("Payment updated successfully.")
        return True

    except Exception as error:
        print(f"Failed updating payment: {error}")
        return False


def add_new_student(id, fname, lname, gender, country, phone, address=None, email=None, university=None, barcode=None):
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
    
def update_student(id, fname, lname, gender, country, phone, address, email, university, barcode):
    cursor = database.cursor()
    try:
        cursor.execute("""
            UPDATE students 
            SET first_name = ?, last_name = ?, gender = ?, country_code = ?, 
                phone_number = ?, address = ?, email = ?, university = ?, barcode = ?
            WHERE id = ?
        """, (fname, lname, gender, country, phone, address, email, university, barcode, id))
        database.commit()
        return True
    except Exception as error:
        print(f"Failed updating student: {error}")
        return False
    
def add_new_doctor(dID, fname, lname, gender, country, phone, email=None):
    cursor = database.cursor()
    try:
        cursor.execute("""
            INSERT INTO doctors (first_name, last_name, gender, country_code, phone_number, email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (fname, lname, gender, country, phone, email))
        database.commit()
        return True
    except Exception as error:
        print(f"Failed creating new doctor: {error}")
        return False
    
def update_doctor(dID, fname, lname, gender, country, phone, email):
    cursor = database.cursor()
    try:
        cursor.execute("""
            UPDATE doctors 
            SET first_name = ?, last_name = ?, gender = ?, country_code = ?, 
                phone_number = ?, email = ?
            WHERE id = ?
        """, (fname, lname, gender, country, phone, email, dID))
        database.commit()
        return True
    except Exception as error:
        print(f"Failed updating doctor: {error}")
        return False
    

def get_id_from_name(table_name, fullname):
    f_name,l_name = fullname.split()
    result = load_data_with_args(From=[table_name],Where=['first_name', 'last_name'], Columns=['id'], Value=[f'"{f_name}"', f'"{l_name}"'])
    result = result[0]
    print(result)
    return result[0]

def add_new_course(cID, name, doc_name, price, s_date, e_date):
    docid = get_id_from_name("doctors", doc_name)
    cursor = database.cursor()
    try:
        cursor.execute("""
                       INSERT INTO courses (name, doctor_id, price, start_date, end_date)
                       VALUES (?, ?, ?, ?, ?)
                       """, (name, docid, price, s_date, e_date))
        database.commit()
        return True
    except Exception as error:
        print(f"Failed creating new course: {error}")
        return False
    
def update_course(cID, name, doc_name, price, s_date, e_date):
    docid = get_id_from_name("doctors", doc_name)
    cursor = database.cursor()
    try:
        cursor.execute("""
            UPDATE courses 
            SET name = ?, doctor_id = ?, price = ?, start_date = ?, end_date = ?
            WHERE id = ?
        """, (name, docid, price, s_date, e_date, cID))
        database.commit()
        return True
    except Exception as error:
        print(f"Failed updating course: {error}")
        return False
    
def delete_course(id):
    cursor = database.cursor()
    try:
        cursor.execute("""
                        DELETE FROM courses
                        WHERE id = ?
                       """, (id,))
        database.commit()
        return True
    except Exception as error:
        print(f"Failed deleting course: {error}")
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

#######################################

# DATA CONTROLLER ####################

def show_error(message: str):
    messagebox.showerror(
            "Invalid Entry",
            message
    )

def student_validate_data(data: dict) -> bool:
    # Ensure required fields are filled with valid data
    message = ""
    if (message := Validation.is_valid_name(data['First Name'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_name(data['Last Name'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_country_code(data['Country Code'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_phone_number(data['Phone Number'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_email(data['Email'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_university(data['University'])) != True:
        show_error(message)
        return False
    # if (message := Validation.is_valid_barcode(data['Barcode'])) != True:
    #     print(message)
    #     return False
    return True

def payment_validate_data(data: dict) -> bool:
    # Example validation: Ensure required fields are filled
    message = ""
    if (message := Validation.is_valid_course_name(data['Course Name'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_payment_amount(data['Paid Amount'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_payment_type(data['Payment Type'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_transaction_date(data['Transaction Date'])) != True:
        show_error(message)
        return False
    return True

def doctor_validate_data(data: dict) -> bool:
    message = ""
    if (message := Validation.is_valid_name(data['First Name'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_name(data['Last Name'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_email(data['Email'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_country_code(data['Country Code'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_phone_number(data['Phone Number'])) != True:
        show_error(message)
        return False
    return True

def func_student(func, entry, data, placeholder):
    # store all new student data in self.data{}
    for key, widget in entry.items():
        # skip image --- just for testing (fix later)
        if key == 'Image':
            continue
        # Handle different widget types
        if isinstance(widget, ttk.Entry):
            value = widget.get()
        elif isinstance(widget, tk.StringVar):
            value = widget.get()
        elif isinstance(widget, ttk.Radiobutton):
            # For radiobuttons, get the value from the associated StringVar
            continue  # Skip individual radiobuttons, use the StringVar stored with the group label
        else:
            value = widget
        data[key] = None
        try:
            if value != placeholder[key]:
                data[key] = value
        except KeyError:
            data[key] = value
    
    if student_validate_data(data):
        if func(
            id = data.get('ID', None),
            fname=data['First Name'],
            lname=data['Last Name'],
            gender=data['Gender'],
            country=data['Country Code'],
            phone=data['Phone Number'],
            email=data['Email'],
            address=data['Address'],
            university=data['University'],
            barcode=data['Barcode']
        ):
            return True
    return False

def delete_student(window, student_id):
    # show confirmation pop_up
    message = "Are you sure you want to delete the student?"
    confirmation_text = "Delete"
    result = PopupHandler.confirmation_popup(window, title="Delete Student", message=message, button1_text="Cancel", button2_text=confirmation_text)
    if result:
        if delete.delete(database, 'students', [student_id]):
            return True
    return False

def func_payment(func, entry):
    # You can now use self.entry to insert the payment into the database or further processing
    pID = entry.get('Payment ID', None)
    sID = entry['Student ID']
    cName = entry['Course Name']
    paid = entry['Paid Amount']
    pay_type = entry['Payment Type']
    tran_date = entry['Transaction Date']
    if payment_validate_data(entry):
        func(
            pID=pID,
            sID=sID,
            course_name=cName,
            paid=paid,
            pay_type=pay_type,
            date=tran_date
        )
        return True
    return False

def delete_payment(window, paymentID):
    title = "Delete Transaction"
    message = "Are you sure?"
    if PopupHandler.confirmation_popup(window, title=title, message=message):
        if delete.delete(database, 'payments', [paymentID]):
            delete.delete_enrollemnts_with_no_payments(database)
            return True
    return False

def load_table(table_name, entry={}):
    # Filter and load matching rows
    if table_name == 'payments':
        columns = [
            "p.id AS ID",
            "sc.course_name AS 'Course Name'",
            "p.amount_paid || ' EGP' AS 'Amount Paid'",
            "p.payment_type AS 'Payment Type'",
            "sc.course_price || ' EGP' AS 'Total'",
            "p.payment_date AS 'Transaction Date'"
        ]
        return load_data_with_args(From=['student_course sc', 'students s', 'payments p'], Where=['s.id', 'p.student_course_id', 's.id'], Value=['sc.student_id', 'sc.id', entry['Student ID']], Columns=columns, Order=['p.payment_date'])
    elif table_name == 'student_course':
        columns = [
            "c.course_name AS 'Course Name'",

            """(c.course_price - IFNULL((
            SELECT SUM(p.amount_paid)
            FROM payments p
            WHERE p.student_course_id = c.id
            ), 0)) || ' EGP' AS Remaining""",

            "c.enrollment_date AS 'Date'"
        ]
        where = [
                    'c.student_id',

                    """(c.course_price - IFNULL((
                    SELECT SUM(p.amount_paid)
                    FROM payments p
                    WHERE p.student_course_id = c.id
                ), 0))
                """
                ]
        return load_data_with_args(From=['student_course c'], Where=where, Value=[entry['Student ID'], 0], Operations=[' = ',' > '], Columns=columns, Order=['c.enrollment_date'])
    elif table_name == 'student_course_all':
        columns = [
            "c.course_name AS 'Course Name'",

            "c.course_price || ' EGP' AS 'Price'",

            """(SELECT SUM(p.amount_paid)
            FROM payments p
            WHERE p.student_course_id = c.id) || ' EGP' AS Paid""",

            """(c.course_price - IFNULL((
            SELECT SUM(p.amount_paid)
            FROM payments p
            WHERE p.student_course_id = c.id
            ), 0)) || ' EGP' AS Remaining""",

            "c.enrollment_date AS 'Enrolled At'"
        ]
        where = [
                    'c.student_id'
                ]
        return load_data_with_args(From=['student_course c'], Where=where, Value=[entry['Student ID']], Operations=[' = '], Columns=columns, Order=['c.enrollment_date'])
    elif table_name == 'courses_report':
        columns = [
            "c.course_name AS 'Course Name'",
            "'Dr.' || d.first_name || ' ' || d.last_name AS 'Doctor Name'",
            "c.course_price AS 'Price'",
            "c.course_start_date AS 'Start Date'",
            "c.course_end_date AS 'End Date'",
            "COUNT(DISTINCT c.student_id) AS 'No Enrolled Students'", 
            "SUM(IFNULL(p.amount_paid, 0)) || ' EGP' AS 'Total Amount Paid'", 
            "((c.course_price*COUNT(DISTINCT c.student_id)) - SUM(IFNULL(p.amount_paid, 0))) || ' EGP' AS 'Total Remaining'", 
            "(c.course_price*COUNT(DISTINCT c.student_id)) || ' EGP' AS 'Total Expected'"
        ]
        where = [
                    '1'
                ]
        group_by = ['c.course_id']
        return load_data_with_args(From=['student_course c LEFT JOIN payments p ON p.student_course_id = c.id JOIN doctors d on d.id = c.doctor_id'], Where=where, Value=['1'], Operations=[' = '], Columns=columns, group=group_by, Order=['c.course_start_date'])
    elif table_name == 'students_with_remaining':
        columns = [
            "s.first_name || ' ' || s.last_name AS 'Student Name'",
            "s.barcode AS 'Barcode'",
            "c.course_name AS 'Course Name'",
            "(c.course_price - IFNULL(SUM(p.amount_paid), 0)) AS 'Remaining Amount'"
        ]
        tables = [
            "student_course c "
            "JOIN students s ON s.id = c.student_id "
            "LEFT JOIN payments p ON p.student_course_id = c.id"
        ]
        where = ["1"]
        group_by = ["s.id", "c.course_id"]
        return load_data_with_args(From=tables, Where=where, Value=["1"], Operations=[" = "], Columns=columns, group=group_by, Order=["'Remaining Amount'"])
    elif table_name == 'doctor_withdraws':
        columns = ['id as ID', 
                   "amount || ' EGP' as Amount", 
                   "withdraw_type as 'Withdraw Method'", 
                   "withdraw_date as 'Date'"
                   ]
        tables = ['withdraws']
        where = ['doctor_id']
        return load_data_with_args(From=tables, Where=where, Value=[entry['Doctor ID']], Columns=columns, Order=['withdraw_date'])
    # elif table_name == 'doctors':
        

def doctor_validate_data(data: dict) -> bool:
    # Example validation: Ensure required fields are filled
    message = ""
    if (message := Validation.is_valid_name(data['First Name'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_name(data['Last Name'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_country_code(data['Country Code'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_phone_number(data['Phone Number'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_email(data['Email'])) != True:
        show_error(message)
        return False
    return True


def func_doctor(func, entry, data, placeholder):
    # store all new doctor data in self.data{}
    for key, widget in entry.items():
        # Handle different widget types
        if isinstance(widget, ttk.Entry):
            value = widget.get()
        elif isinstance(widget, tk.StringVar):
            value = widget.get()
        elif isinstance(widget, ttk.Radiobutton):
            # For radiobuttons, get the value from the associated StringVar
            continue  # Skip individual radiobuttons, use the StringVar stored with the group label
        else:
            value = widget
        data[key] = None
        try:
            if value != placeholder[key]:
                data[key] = value
        except KeyError:
            data[key] = value

    if doctor_validate_data(data):
        if func(
            dID=data.get('ID', None),
            fname=data['First Name'],
            lname=data['Last Name'],
            gender=data['Gender'],
            country=data['Country Code'],
            phone=data['Phone Number'],
            email=data['Email']
        ):
            return True
    return False
        
def delete_doctor(window, data):
    # show confirmation pop_up
    message = "Are you sure you want to delete this doctor?"
    confirmation_text = "Delete"
    result = PopupHandler.confirmation_popup(window, title="Delete Doctor", message=message, button1_text="Cancel", button2_text=confirmation_text)
    if result:
        if delete.delete(database, 'doctors', [data['ID']]):
            return True
    return False

def course_validate_data(data: dict) -> bool:
    # Example validation: Ensure required fields are filled
    message = ""
    if (message := Validation.is_valid_course_name(data['Course Name'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_doctor_name(data['Doctor Name'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_payment_amount(data['Price'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_start_date(data['Start Date'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_end_date(data['End Date'])) != True:
        show_error(message)
        return False
    return True

def func_course(func,entry,data,placeholder):
    # store all new course data in self.data{}
    for key, widget in entry.items():
        # DatePicker (custom)
        if hasattr(widget, "entry") and isinstance(getattr(widget, "entry"), ttk.Entry):
            # e.g. DatePicker: .entry is the underlying entry widget
            value = widget.entry.get().strip()
        elif isinstance(widget, tk.StringVar):
            value = widget.get()
        elif isinstance(widget, ttk.Entry):
            value = widget.get()
        elif isinstance(widget, ttk.Combobox):
            value = widget.get()
        else:
            # fallback: whatever the widget is (e.g., radiobutton group stringvar earlier)
            try:
                value = widget.get()
            except Exception:
                value = widget

        # store values into data
        data[key] = None
        try:
            if value != placeholder[key]:
                data[key] = value
        except KeyError:
            data[key] = value

    if course_validate_data(data):
        if func(
            cID=data['ID'],
            name=data['Course Name'],
            doc_name=data['Doctor Name'],
            price=data['Price'],
            s_date=data['Start Date'],
            e_date=data['End Date']
            ):
                return True
    return False

def delete_course(window, data):
    # show confirmation pop_up
    message = "Are you sure you want to delete this course?"
    confirmation_text = "Delete"
    result = PopupHandler.confirmation_popup(window, title="Delete Course", message=message, button1_text="Cancel", button2_text=confirmation_text)
    if result:
        if delete.delete(database, 'courses', [data['ID']]):
            return True
    return False


def select_unregistered_courses(s_id):
    return select.select_unregistered_courses(database, s_id).fetchall()