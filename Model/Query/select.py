def select(database, table_name, relations=[], *columns):
    keys = table_name
    conditions = ""
    for i, relation in enumerate(relations):
        if i == 0:
            conditions = "WHERE "
        keys += ", "
        keys += relation[0]
        conditions += relation[1]
        if len(relations)-i-1:
            relation += ", "
    selected_columns = ""
    for i,col in enumerate(columns):
        selected_columns += col
        if len(columns)-i-1:
            selected_columns += ", "
    
    if selected_columns == "":
        selected_columns = "*"

    query = f"""
        SELECT {selected_columns}
        FROM {keys}
        {conditions}
        ORDER BY id DESC;
    """
    # print(query)
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
            ), 0)) || ' EGP' AS Remaining,
            c.enrollment_date AS 'Date'
        FROM student_course c
        WHERE c.student_id = {ID}
        AND (c.course_price - IFNULL((
            SELECT SUM(p.amount_paid)
            FROM payments p
            WHERE p.student_course_id = c.id
        ), 0)) > 0;
    """
    cursor = database.cursor()
    cursor.execute(query)
    database.commit()
    return cursor

def select_for_student_transactions(database, ID):
    query = f"""
        SELECT 
            p.id AS ID,
            sc.course_name AS 'Course Name', 
            p.amount_paid || ' EGP' AS 'Amount Paid', 
            p.payment_type AS 'Payment Type', 
            sc.course_price || ' EGP' AS 'Total',
            p.payment_date AS 'Transaction Date'
        FROM students s
        JOIN student_course sc ON s.id = sc.student_id
        JOIN payments p ON p.student_course_id = sc.id
        WHERE s.id = {ID}
        ORDER BY p.payment_date DESC;
    """
    cursor = database.cursor()
    cursor.execute(query)
    database.commit()
    return cursor

def select_unregistered_courses(database, ID):
    query = f"""
        SELECT c.name AS 'Course Name', c.price
        FROM courses c
        WHERE c.id NOT IN (
            SELECT sc.course_id
            FROM student_course sc
            WHERE sc.student_id = {ID}
        )
        AND c.start_date <= DATE('now')
        AND c.end_date >= DATE('now');
    """
    cursor = database.cursor()
    cursor.execute(query)
    database.commit()
    return cursor

def select_doctors(database, *columns):
    selected_columns = ""
    for i,col in enumerate(columns):
        selected_columns += col
        if len(columns)-i-1:
            selected_columns += ", "

    query = f"""
    SELECT {selected_columns}
    FROM doctors;
    """
    cursor = database.cursor()
    cursor.execute(query)
    database.commit()
    return cursor

def select_with_args(database, columns, froms, conditions, group, order):
    try:
        query = f"""
            SELECT {columns}
            FROM {froms}
            WHERE {conditions}
        """
        if len(group) > 0:
            query += f"    GROUP BY {group}\n"
        if len(order) > 0:
            query += f"    ORDER BY {order} DESC\n"
            
        cursor = database.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as error:
        return None