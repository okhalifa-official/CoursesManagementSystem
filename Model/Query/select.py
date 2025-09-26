
def student_select_special(database):
    query = """
        SELECT s.id AS id, s.name AS Student, c.name AS Course, d.name AS Doctor, payments.id AS 'Payment ID'
        FROM payments, students s JOIN student_enrollment ss ON s.id = ss.student_id
        JOIN courses c ON ss.course_id = c.id
        JOIN doctors d ON c.doctor_id = d.id
        WHERE payments.course_id = c.id AND payments.student_id = s.id
        ORDER BY s.id
    """
    cursor = database.cursor()
    cursor.execute(query)
    database.commit()
    return cursor

def select(database, table_relation):
    #table_relation = [('students', 'id'), ('courses', 'student_id')]
    query = f"""
        SELECT *
        FROM {table_relation[0][0]}
    """
    for i in range(1,len(table_relation)):
        query += f"""
            JOIN {table_relation[i][0]}
            ON {table_relation[i-1][0]}.{table_relation[i-1][1]} = {table_relation[i][0]}.{table_relation[i][1]}
        """
    cursor = database.cursor()
    cursor.execute(query)
    database.commit()
    return cursor

# select a record by ID from the given table (table_name)
def select_by_id(database, table_name, ID):
    query = f"""
        SELECT *
        FROM {table_name}
        WHERE id = {ID}
    """
    cursor = database.cursor()
    cursor.execute(query)
    database.commit()
    return cursor


# select all enrolled courses with their remaining amount and date of enrollment
def select_for_course_payment_table(database, ID):
    query = f"""
        SELECT 
            c.course_name AS 'Course Name', 
            (c.course_price - IFNULL((
                SELECT SUM(p.amount_paid)
                FROM payments p
                WHERE p.student_course_id = c.id
            ), 0)) AS Remaining,
            c.enrollment_date AS 'Date'
        FROM student_course c
        WHERE c.student_id = {ID};
    """
    cursor = database.cursor()
    cursor.execute(query)
    database.commit()
    return cursor

def select_for_student_transactions(database, ID):
    query = f"""
        SELECT 
            sc.course_name AS 'Course Name', 
            p.amount_paid AS 'Amount Paid', 
            p.payment_type AS 'Payment Type', 
            sc.course_price AS 'Total',
            p.payment_date AS 'Transaction Date'
        FROM students s
        JOIN student_course sc ON s.id = sc.student_id
        JOIN payments p ON p.student_course_id = sc.id
        WHERE s.id = {ID};
    """
    cursor = database.cursor()
    cursor.execute(query)
    database.commit()
    return cursor
