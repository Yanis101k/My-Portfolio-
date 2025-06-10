import unittest 
import sqlite3 # Built-in Python module to intercat with SQLite databases 

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

# Set environment variable to use a temporary database
os.environ["DATABASE_PATH"] = "database/test_portfolio.db"

from database.connector import DatabaseConnector # Manages SQLite connection
from database.project_dao import ProjectDAO # DAO to test
from models.project import Project # Project model for input / output 

class TestProjectDAO(unittest.TestCase):
    '''
    ✅ Unit test class for ProjectDAO
    Uses a temporary database file to test full CRUD functionality.
    '''

    def setUp(self):
        '''
        ✅ This runs before each test. It creates:
        - a fresh test DB
        - a DB connection
        - tables using schema.sql
        - DAO instance
        '''
        # Create and connect to test database
        self.db = DatabaseConnector()
        self.conn = self.db.connect()

        # ✅ Load schema to create tables
        with open("database/schema.sql", "r") as f:
            self.conn.executescript(f.read())

        self.dao = ProjectDAO(self.db)

    def tearDown(self):
        '''
        ✅ Runs after each test to close DB and delete test database file
        '''
        self.db.close()
        if os.path.exists("database/test_portfolio.db"):
            os.remove("database/test_portfolio.db")

    def test_add_and_get_project(self):
        '''
        ✅ Test creating and retrieving a single project
        '''

        
        # Add a sample project
        project = Project(None, "Test Title", "Test Description", "img.png", "https://github.com/test", "https://live.com")
        self.dao.add_project(project)

        # Retrieve all projects
        projects = self.dao.get_all_projects()
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0].get_title(), "Test Title")
    

    def test_get_project_by_id(self):
        '''
        ✅ Test retrieving a project by its ID
        '''
        # insert three project and after that try to find the project from those three project using its id 
         # Add project to find 
        project = Project(None, "title project 1", "description project 1", None, None, None)
        self.dao.add_project(project)
        
        # Add project to find 
        project = Project(None, "Find Me", "To find by ID", None, None, None)
        self.dao.add_project(project)

         # Add project to find 
        project = Project(None, "title project 2", "description project 2", None, None, None)
        self.dao.add_project(project)

        # Fetch the inserted project’s ID
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM projects WHERE title = ?", ("Find Me",))
        result = cursor.fetchone()
        project_id = result[0]

        found = self.dao.get_project_by_id(project_id)
        self.assertIsNotNone(found)
        self.assertEqual(found.get_id(), project_id ) 
        self.assertEqual(found.get_title(), "Find Me") 
        self.assertEqual(found.get_description(), "To find by ID") 
    
    
    def test_update_project(self):
        '''
        ✅ Test updating an existing project
        '''

        # Add project
        unchangeable_project1 = Project( 1 , "unchangeable title 1 ", "unchangeable description 1", None, None, None)
        self.dao.add_project(unchangeable_project1)

        # Add project
        project_to_update = Project( None , "Old Title", "Old Description", None, None, None)
        self.dao.add_project(project_to_update)

        # Add project
        unchangeable_project2 = Project( 3 , "unchangeable title 2", "unchangeable title 2", None, None, None)
        self.dao.add_project(unchangeable_project2)

        # Get its ID
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM projects WHERE title = ?", ("Old Title",))
        project_id = cursor.fetchone()[0]

        # Update the project
        updated = Project(project_id, "New Title", "New Description", None, None, None)
        self.dao.update_project(updated)

        # Fetch it again to check if it updated 
        fetched = self.dao.get_project_by_id(project_id)
        self.assertEqual(fetched.get_title(), "New Title")
        self.assertEqual(fetched.get_description(), "New Description")

        
        # Fetch other projects to check if they remain the same
        unchangeable_project = self.dao.get_project_by_id( 1 )
        self.assertEqual( unchangeable_project.get_title() , unchangeable_project1.get_title() )
        self.assertEqual( unchangeable_project.get_description() , unchangeable_project1.get_description() )

        unchangeable_project = self.dao.get_project_by_id( 3 )
        self.assertEqual( unchangeable_project.get_title() , unchangeable_project2.get_title() )
        self.assertEqual( unchangeable_project.get_description() , unchangeable_project2.get_description() )

    def test_delete_project(self):

        '''
        ✅ Test deleting a project by ID
        '''

        # Add project
        project_not_to_delete1 = Project(None, "project to not delete title 1", "project to not delete description 1", None, None, None)
        self.dao.add_project(project_not_to_delete1 )

        # Add project
        project_to_delete = Project(None, "Delete Me", "To be deleted", None, None, None)
        self.dao.add_project( project_to_delete )

        # Add project
        project_not_to_delete2 = Project(None, "project to not delete title 2", "project to not delete description 2", None, None, None)
        self.dao.add_project( project_not_to_delete2 )

        # Get its ID
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM projects WHERE title = ?", ("Delete Me",))
        project_to_delete_id = cursor.fetchone()[0]

        # Delete the project
        self.dao.delete_project(project_to_delete_id)


 
        # Try to fetch it again and be sure it deleted 
        deleted = self.dao.get_project_by_id(project_to_delete_id)
        self.assertIsNone(deleted)

        # be sur others projects are not deleted 

        # get the id of the first project that should not be deleted 
        cursor.execute("SELECT id FROM projects WHERE title = ? " , ("project to not delete title 1",) )
        project_not_to_delete_id = cursor.fetchone()[0]
        project_not_to_delete = self.dao.get_project_by_id( project_not_to_delete_id )
        self.assertIsNotNone(project_not_to_delete)

        # get the id of the second project that should not be deleted 
        project_not_to_delete_id =  cursor.execute("SELECT id FROM projects WHERE title = ? " , ("project to not delete title 2",) )
        project_not_to_delete_id = cursor.fetchone()[0]
        project_not_to_delete = self.dao.get_project_by_id( project_not_to_delete_id )
        self.assertIsNotNone(project_not_to_delete)





if __name__ == '__main__':
    unittest.main()