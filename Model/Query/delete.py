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