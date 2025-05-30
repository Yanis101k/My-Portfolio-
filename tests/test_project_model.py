import unittest  # Built-in Python module used to create and run unit tests 

#The sys module allows you to interact with the Python interpreter itself. It's useful for handling system-specific information 
# and controlling the program's behavior.
# Add path for module search
import sys

#The os module in Python gives you access to operating system features like : 
#reading or writing files, navigating folders, and managing environment variables.
import os


# Make root directory visible to Python so we can import project.py model
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the Project  class from models folder 
from models.project import Project 

"""
This class contains tests for the Project model . 
it verifies tha the Project class correctly encapsulates data and 
behaves as expected 
"""


class TestProjectModel( unittest.TestCase ) : 
    
    def setUp( self ):
    
        """
        This method run before every test 
        it sets a sample Project object to be reused across tests 
        """

        self.project = Project (
            id = 1 , 
            title="Task tracker", 
            description="A web app to track tasks",
            image_url="images/task.png",
            github_url="https://github.com/Yanis101k/tasks-tracker",
            live_url="http://localhost:5000/project/",
            created_at="2024-01-01 10:00:00"
        ) 

    
    def test_getters(self):

        """
        Test that all getters return the expected values 
        """
        
        self.assertEqual( self.project.get_id() , 1 )
        self.assertEqual(self.project.get_title() , "Task tracker")
        self.assertEqual(self.project.get_description() , "A web app to track tasks")
        self.assertEqual(self.project.get_github_url() , "https://github.com/Yanis101k/tasks-tracker")
        self.assertEqual(self.project.get_live_url(), "http://localhost:5000/project/")
        self.assertEqual(self.project.get_created_at() , "2024-01-01 10:00:00")

    
    def test_setters(self):
            """
            Test that all setter methods correctly update internal values.
            """
            self.project.set_title("Updated Title")
            self.project.set_description("Updated Description")
            self.project.set_image_url("new/image.png")
            self.project.set_github_url("https://github.com/updated")
            self.project.set_live_url("http://localhost/updated")

            self.assertEqual(self.project.get_title(), "Updated Title")
            self.assertEqual(self.project.get_description(), "Updated Description")
            self.assertEqual(self.project.get_image_url(), "new/image.png")
            self.assertEqual(self.project.get_github_url(), "https://github.com/updated")
            self.assertEqual(self.project.get_live_url(), "http://localhost/updated")

    
    def test_to_dict(self) : 
        """
        Test that the to_dict method correctly converts the object to a dictionary.
        """
        expected = {
                "id": 1,
                "title": "Task tracker",
                "description": "A web app to track tasks",
                "image_url": "images/task.png",
                "github_url": "https://github.com/Yanis101k/tasks-tracker",
                "live_url": "http://localhost:5000/project/",
                "created_at": "2024-01-01 10:00:00"
            }
        self.assertEqual(self.project.to_dict(), expected)
        

# Run the tests if this file is executed directly
if __name__ == '__main__':
    unittest.main()
