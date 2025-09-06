import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Model', 'Query'))

from DB import db # type: ignore
from Model.Query import select

database = db()

def load_data(table_name):
    tables_relations = [(table_name, '')]
    try:
        select.select(database, tables_relations)
    except Exception as error:
        print(f"Failed loading data: {error}")
        return None
    
    rows = database.fetchall()
    return rows
