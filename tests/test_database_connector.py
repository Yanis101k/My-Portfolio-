import unittest  # ✅ Used for writing and running test cases

# ✅ Used to set environment variables during testing
#The sys module allows you to interact with the Python interpreter itself. It's useful for handling system-specific information 
# and controlling the program's behavior.
# Add path for module search
import sys

#The os module in Python gives you access to operating system features like : 
#reading or writing files, navigating folders, and managing environment variables.
import os

# Make root directory visible to Python so we can import config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlite3   # ✅ To verify database file creation
from database.connector import DatabaseConnector  # ✅ Class under test

# 🔧 Set up a temporary test database path in the environment
os.environ["DATABASE_PATH"] = "database/test_portfolio.db"

class TestDatabaseConnector(unittest.TestCase):
    """
    Unit tests for the DatabaseConnector class using a temporary test database.
    """

    def setUp(self):
        """
        This runs before each test. It initializes a DatabaseConnector instance.
        """
        self.db = DatabaseConnector()

    def tearDown(self):
        """
        This runs after each test. It closes the DB connection and deletes the temp file.
        """
        self.db.close()
        if os.path.exists("database/test_portfolio.db"):
            os.remove("database/test_portfolio.db")

    def test_connection_establishment(self):
        """
        Test if the connector creates a valid SQLite connection.
        """
        connection = self.db.connect()
        self.assertIsInstance(connection, sqlite3.Connection)  # ✅ Asserts correct type
        self.assertFalse(connection is None)  # ✅ Ensure connection was actually created

    def test_multiple_get_connection_calls(self):
        """
        Test that calling get_connection() multiple times returns the same connection.
        """
        conn1 = self.db.connect()
        conn2 = self.db.connect()
        self.assertIs(conn1, conn2)  # ✅ Should return same connection object

    def test_connection_close(self):
        """
        Test if the connection closes properly and becomes None internally.
        """
        self.db.connect()
        self.db.close()

        # check if the connection really closed and becomes none internally 
        self.assertIsNone(self.db.get_connection() )  

# Run the tests if this file is executed directly
if __name__ == '__main__':
    unittest.main()