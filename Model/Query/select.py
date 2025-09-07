
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