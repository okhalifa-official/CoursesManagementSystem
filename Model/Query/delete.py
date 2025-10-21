def delete(database, table, ids):
    query = f"""
        DELETE FROM {table}
        WHERE id = {ids[0]}
    """
    for i in range(1,len(ids)):
        query += f"OR id = {ids[i]} "
    cursor = database.cursor()
    try:
        cursor.execute(query)
        database.commit()
        return True
    except Exception as error:
        print(f"Failed deleting records: {error}")
        return False

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
    try:
        cursor.execute(query)
        database.commit()
        return True
    except Exception as error:
        print(f"Failed deleting enrollments with no payments: {error}")
        return False