from sqlite3 import OperationalError

from database.db_connection import get_db_connection
from config import DB_CMDS_PATH

def execute_script_from_file(cursor, filepath):
    '''Fetches an sql file and executes the queries specified in it.

    args:
        cursor: SQLite cursor
        filename: path to the executable file
    '''

    sql_file = open(filepath, 'r')
    data = sql_file.read()
    sql_file.close()

    queries = data.split(';')
    for query in queries:
        try:
            cursor.execute(query)
        except OperationalError:
            print(f'query "{query}" skipped')

def populate_db(conn):
    '''Creates tables storing default information in the game database.'''
    cursor = conn.cursor()
    execute_script_from_file(cursor, DB_CMDS_PATH)
    conn.commit()

def drop_tables(conn):
    '''Clears the game database if one exists.'''
    tables = [
        'Items', 'Skills', 'Effects', 'ItemEffects',
        'SkillEffects', 'Monsters', 'Party',
        'Stats', 'Resistance', 'CharSkills', 'Loot',
        'Inventory'
        ]
    cursor = conn.cursor()
    for table in tables:
        statement = f'DROP TABLE IF EXISTS {table}'
        cursor.execute(statement)
    conn.commit()

def initialise_db():
    '''Initialises the game database.'''
    conn = get_db_connection()
    drop_tables(conn)
    populate_db(conn)

if __name__ == '__main__':
    initialise_db()
