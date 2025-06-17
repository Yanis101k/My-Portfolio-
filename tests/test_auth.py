import unittest
import os
import sys
import json

# Add project root to sys.path BEFORE importing app/config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load .env.test before importing Config or app
from dotenv import load_dotenv
env_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '.env.test')
load_dotenv(dotenv_path=env_path)

# Now import Config and app
from config import Config
from app import app
from flask import session


class AuthSystemTestCase(unittest.TestCase):
    def setUp(self):

        """
        This method runs before every test.
        It sets up the Flask test client and enables testing mode.
        """
        app.config['TESTING'] = True
        app.secret_key = Config.get_secret_key()  # for session signing
        self.client = app.test_client()
        app.config['DEBUG'] = True
    
    def login(self, username, password):
        """
        Helper function to simulate a login request.
        """
        return self.client.post('/api/login', json={
            'username': username,
            'password': password
        })

    def logout(self):
        """
        Helper function to simulate a logout request.
        """
        return self.client.post('/api/logout')

    def test_valid_login(self):
        """
        Test that valid credentials return a success message and status code 200.
        """
       
        response = self.login( Config.get_admin_username() , "b")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login successful", response.get_data(as_text=True))

    def test_invalid_login_wrong_password(self):
         """
         Test that a wrong password results in a 401 Unauthorized status.
         """
         response = self.login(Config.get_admin_username() , "wrongpassword")
         self.assertEqual(response.status_code, 401)
         self.assertIn("Invalid username or password", response.get_data(as_text=True))

    def test_login_missing_fields(self):
         """
       Test that missing username or password returns a 400 Bad Request.
         """
         response = self.client.post('/api/login', json={})
         self.assertEqual(response.status_code, 400)
         

    def test_login_wrong_data_type(self):
        """
         Test that sending numbers instead of strings returns a 400 error.
         """
        response = self.client.post('/api/login', json={"username": 123, "password": True})
        self.assertEqual(response.status_code, 400)
        self.assertIn("must be strings", response.get_data(as_text=True))

    # def test_crud_operations_authenticated(self):
    #      # Login first
    #      self.login( Config.get_admin_username() , "b")

    #      # Create
    #      create_response = self.client.post('/api/projects', json={
    #          "title": "Test Project",
    #          "description": "CRUD test project",
    #          "image_url": "http://example.com/image.png",
    #          "github_url": "http://github.com/test/project",
    #          "live_url": "http://example.com/project"
    #      })
    #      self.assertEqual(create_response.status_code, 201)
    #      project_id = create_response.get_json().get("id", 1)  # default to 1 for test

    #      # Read all
    #      read_all = self.client.get('/api/projects')
    #      self.assertEqual(read_all.status_code, 200)

    #      # Read specific
    #      read_one = self.client.get(f'/api/projects/{project_id}')
    #      self.assertEqual(read_one.status_code, 200)

    #      # Update
    #      update_response = self.client.put(f'/api/projects/{project_id}', json={
    #          "title": "Updated Project",
    #          "description": "Updated description"
    #      })
    #      self.assertIn(update_response.status_code, [200, 204])  # accept 204 (no content) too

    #      # Delete
    #      delete_response = self.client.delete(f'/api/projects/{project_id}')
    #      self.assertIn(delete_response.status_code, [200, 204])

    # def test_crud_operations_unauthenticated(self):
    #      # Try CREATE
    #      create = self.client.post('/api/projects', json={
    #          "title": "Blocked",
    #          "description": "Should not be created"
    #      })
    #      self.assertEqual(create.status_code, 401)

    #     # Try UPDATE
    #      update = self.client.put('/api/projects/1', json={
    #          "title": "Blocked Update"
    #      })
    #      self.assertEqual(update.status_code, 401)

    #      # Try DELETE
    #      delete = self.client.delete('/api/projects/1')
    #      self.assertEqual(delete.status_code, 401)

if __name__ == '__main__':
    unittest.main()