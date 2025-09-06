def insert(database, table, values):
        #table = (tb_namem,[col1, col2, col3])
        #values = [col1, col2, col3]
        table_name, columns = table
        placeholders = ",".join("?" for _ in columns)
        query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"

        database.cursor().execute(query, values)
        database.commit()