import sqlite3
from config import DB_PATH

def get_db_connection(db=DB_PATH):
    '''Returns connection to the game database.'''
    # move to db_util
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn
