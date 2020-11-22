import sqlite3
from sqlite3 import Error

def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect('attendance.db')
    except Error as e:
        print(e)
    return conn
