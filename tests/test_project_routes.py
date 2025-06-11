import unittest
import sqlite3 # Built-in Python module to interact with SQLite databases

# the sys module allow us to interact with the Python interpreter . it's useful for handling system-specific information
#and controlling the program's behavior 
#Add path for module search 
import sys 

# the os module in python gives you access to operating system features like : 
# reading or writing files , navigating folders , and managing environment variables.
# Used to set environment variables during testing 

import os 

#  Make root directory visible to python se we can import config.py
sys.path.append( os.path.abspath( os.path.join( os.path.dirname(__file__) , '..' )))

# Set environment variable to use a temporary database
os.environ["DATABASE_PATH"] = "database/test_portfolio.db"

from database.connector import DatabaseConnector # Manages SQLite connection
from database.project_dao import ProjectDAO # class that interact with the databse directly using sql 
from models.project import Project # project model for output and input 
from controllers.project_controller import ProjectController # class to test 
from flask import Flask
from app import app 

class GetAllProjectsRouteTest(unittest.TestCase):
    def setUp(self):
        """
            This run before each test. It creates : 
            - a fresh test DB
            - a DB connection 
            - tables using schema.sql
            - ProjectController instance 
        """

        # ✅ Configure app for testing
        app.config["TESTING"] = True
        self.client = app.test_client()

        # Create and connect to test database
        self.db = DatabaseConnector()
        self.conn = self.db.connect() 

        # Load schema to create tables 
        with open("database/schema.sql" , "r" ) as f : 
            self.conn.executescript(f.read())

        self.dao = ProjectDAO(self.db)
    
    def tearDown(self):
        """
           Runs after each test to close DB and delet test databse file 
        """  
        self.db.close()
    

    def test_get_all_projects_empty(self):
        # ✅ Test when no projects exist
        response = self.client.get("/api/projects")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(response.json["data"], [])

    def test_get_all_projects_with_data(self):
        # ✅ Insert sample project into the test DB
        sample_project = Project(
            id=None,
            title="Sample Title",
            description="Sample Description",
            image_url=None,
            github_url=None,
            live_url=None
        )
        self.dao.add_project(sample_project)

        # ✅ Test when project exists
        response = self.client.get("/api/projects")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(response.json["data"][0]["title"], "Sample Title")

    def test_get_project_by_valid_id(self):
        # ✅ Insert one project
        project = Project(None, "Valid Project", "Description", None, None, None)
        self.dao.add_project( project )

        # ✅ Get the actual ID
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM projects WHERE title = ?", ("Valid Project",))
        project_id = cursor.fetchone()[0]

        # ✅ Test the route
        response = self.client.get(f"/api/projects/{project_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(response.json["data"]["title"], "Valid Project")

    def test_get_project_by_invalid_id(self):
        # ✅ Use an ID that does not exist
        response = self.client.get("/api/projects/9999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["status"], "error")
        self.assertIn("not found", response.json["message"].lower())
        
        # ✅ Use an ID that is not invalid string type
        response = self.client.get("/api/projects/qflm")
        self.assertEqual(response.status_code, 404)


    
    def test_create_project_success(self):
        payload = {
            "title": "My Test Project",
            "description": "A project created in test",
            "image_url": None,
            "github_url": None,
            "live_url": None
        }

        response = self.client.post("/api/projects", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["status"], "success")
        self.assertIn("created", response.json["message"].lower())

        # 🔎 Optional: check that it was actually inserted into the DB
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM projects WHERE title = ?", ("My Test Project",))
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)
    
    def test_update_project_success(self):
        # Add a project first
        original = Project(None, "Old Title", "Old Desc", None, None, None)
        self.dao.add_project(original)

        # Get its ID
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM projects WHERE title = ?", ("Old Title",))
        project_id = cursor.fetchone()[0]

        # Update it
        updated_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "image_url": None,
            "github_url": None,
            "live_url": None
        }

        response = self.client.put(f"/api/projects/{project_id}", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

        # Confirm change in DB
        cursor.execute("SELECT title FROM projects WHERE id = ?", (project_id,))
        self.assertEqual(cursor.fetchone()[0], "Updated Title")

    def test_update_project_not_found(self):
        updated_data = {
            "title": "Doesn't Matter",
            "description": "No project has this ID",
            "image_url": None,
            "github_url": None,
            "live_url": None
        }
        response = self.client.put("/api/projects/9999", json=updated_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["status"], "error")
    
    def test_delete_existing_project(self):
        # Add project first
        project = Project(None, "To Delete", "Will be deleted", None, None, None)
        self.dao.add_project(project)

        # Get ID
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM projects WHERE title = ?", ("To Delete",))
        project_id = cursor.fetchone()[0]

        # Send DELETE request
        response = self.client.delete(f"/api/projects/{project_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

        # Confirm it’s deleted
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        self.assertIsNone(cursor.fetchone())

    def test_delete_nonexistent_project(self):
        response = self.client.delete("/api/projects/9999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["status"], "error")
        self.assertIn("not found", response.json["message"].lower())

    def test_delete_invalid_id(self):
        response = self.client.delete("/api/projects/invalid_id")
        self.assertEqual(response.status_code, 404)  # Flask route not matched


    
    # think about those valid input tests later when you impliment
    """
        def test_update_project_invalid_data(self):
        # Add a project to update
        project = Project(None, "Safe Title", "Safe Desc", None, None, None)
        self.dao.add_project(project)

        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM projects WHERE title = ?", ("Safe Title",))
        project_id = cursor.fetchone()[0]

        # Send completely invalid data (string instead of JSON)
        response = self.client.put(f"/api/projects/{project_id}", data="not json", content_type="application/json")
        self.assertEqual(response.status_code, 500)  # Or 400 if controller handles JSON errors

    """

    """
    def test_create_project_missing_fields(self):
        payload = {
            "title": "Only title provided"
        }

        response = self.client.post("/api/projects", json=payload)
        self.assertIn(response.status_code, [400, 500])  # 400 if controller handles it, 500 if it crashes
        self.assertEqual(response.json["status"], "error")

    def test_create_project_invalid_json(self):
        # 🔹 Send malformed (non-JSON) payload
        response = self.client.post("/api/projects", data="not a json", content_type="application/json")
        self.assertEqual(response.status_code, 500)  # Or 400 if manually handled
        self.assertEqual(response.json["status"], "error")
    """

if __name__ == "__main__":
    unittest.main()


