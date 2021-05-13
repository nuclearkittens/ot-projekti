import sqlite3
from config import DB_PATH

def get_db_connection():
    '''Returns connection to the game database.

    args:
        db: path to database to be used
    '''
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
