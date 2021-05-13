import unittest
import sqlite3

from database.db_connection import get_db_connection
from database.initialise_db import drop_tables

class TestDbConnection(unittest.TestCase):
    def test_get_db_connection(self):
        conn = get_db_connection()
        self.assertIsInstance(conn, sqlite3.Connection)
        drop_tables(conn)
        conn.close()
