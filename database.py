import sqlite3
import shared
import os


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


def overwrite_db():
    response = input(
        'Do you really want to overwrite the entire database? Y/N: ').lower()

    if not response == 'y':
        print('Did not overwrite database.')
        return None
    try:
        os.remove(shared.db_name)
    except:
        pass
    with open('tables.txt') as f:
        tables = [i + ';' for i in f.read().split(';')]
    for i in tables:
        write_db(i)
