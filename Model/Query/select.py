
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
        
        database.execute(query)
        database.commit()