def delete(database, table, ids):
    query = f"""
        DELETE FROM {table}
        WHERE id = {ids[0]}
    """
    for i in range(1,len(ids)):
        query += f"OR id = {ids[i]} "
    cursor = database.cursor()
    cursor.execute(query)
    database.commit()

def delete_enrollemnts_with_no_payments(database):
    query = """
        DELETE FROM student_course
        WHERE id NOT IN (
            SELECT DISTINCT student_course_id
            FROM payments
            WHERE student_course_id IS NOT NULL
        );
    """
    cursor = database.cursor()
    cursor.execute(query)
    database.commit()
