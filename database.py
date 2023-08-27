import sqlite3
import shared

def read_db(query, params=None):
    conn = sqlite3.connect(shared.db_name)
    c = conn.cursor()

    if params:
        c.execute(query, params)
    else:
        c.execute(query)
    column_names = [description[0] for description in c.description]
    rows = c.fetchall()
    rows.insert(0, column_names)
    conn.close()
    return rows

def write_db(query, params=None):
    conn = sqlite3.connect(shared.db_name)
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    conn.close()
    
def insert_db(query, data):
    conn = sqlite3.connect(shared.db_name)
    cursor = conn.cursor()

    try:
        cursor.executemany(query, data)
    except AttributeError:
        pass
    conn.commit()
    conn.close()