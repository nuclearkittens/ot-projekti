import sqlite3
from config import DB_PATH

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

def get_db_connection():
    '''Returns connection to the game database.'''
    return conn
