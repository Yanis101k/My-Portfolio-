import sqlite3  # Built-in Python module to interact with SQLite databases
import logging   # Used to log messages for debugging and monitoring 
import sys       # Allows interacting with the Python interpreter
import os        # Access to OS features like files, paths, and environment variables

# Make root directory visible to Python so we can import project model
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.project import Project                # Import the Project model
from database.connector import DatabaseConnector  # Import database connection class

class ProjectDAO:
    """
    DAO (Data Access Object) class for handling all database operations (CRUD)
    related to Project entities. Follows clean separation of concerns by
    keeping SQL logic out of the business logic (Controller/Model).
    """

    def __init__(self, db_connector: DatabaseConnector):
        """
        Constructor: Initialize the DAO with an existing database connection.
        :param db_connector: An instance of DatabaseConnector class
        """
        self.logger = logging.getLogger(__name__)
        self.connection = db_connector.connect()

    def get_all_projects(self):
        """
        Retrieve all projects from the database.
        :return: List of Project objects or an empty list if no projects exist
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM projects")
            rows = cursor.fetchall()
            if not rows:
                self.logger.info("No projects found in the database.")
                return []
            projects = [Project(*row) for row in rows]
            self.logger.info(f"{len(projects)} projects fetched from the database.")
            return projects
        except sqlite3.Error as e:
            self.logger.error(f"Error fetching projects: {e}")
            raise

    def get_project_by_id(self, project_id: int):
        """
        Retrieve a single project by its unique ID.
        :param project_id: Integer ID of the project
        :return: A Project object or None if not found
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
            row = cursor.fetchone()
            if row:
                self.logger.info(f"Project {project_id} found.")
                return Project(*row)
            else:
                self.logger.warning(f"Project {project_id} not found.")
                return None
        except sqlite3.Error as e:
            self.logger.error(f"Error fetching project by ID: {e}")
            raise

    def add_project(self, project: Project):
        """
        Insert a new project record into the database.
        :param project: An instance of the Project model
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO projects (title, description, image_url, github_url, live_url)
                VALUES (?, ?, ?, ?, ?)""",
                (
                    project.get_title(),
                    project.get_description(),
                    project.get_image_url(),
                    project.get_github_url(),
                    project.get_live_url()
                ))
            self.connection.commit()
            self.logger.info("New project inserted successfully.")
        except sqlite3.Error as e:
            self.logger.error(f"Error inserting project: {e}")
            raise

    def update_project(self, project: Project) -> bool:
        """
        Update an existing project's information.
        :param project: A Project object with updated fields (must include its ID)
        :return: True if updated successfully, False if not found
        """
        try:
            cursor = self.connection.cursor()
            result = cursor.execute("""
                UPDATE projects
                SET title = ?, description = ?, image_url = ?, github_url = ?, live_url = ?
                WHERE id = ?
            """,
                (
                    project.get_title(),
                    project.get_description(),
                    project.get_image_url(),
                    project.get_github_url(),
                    project.get_live_url(),
                    project.get_id()
                ))
            self.connection.commit()
            if result.rowcount == 0:
                self.logger.warning(f"Project {project.get_id()} not found for update.")
                return False
            self.logger.info(f"Project {project.get_id()} updated.")
            return True
        except sqlite3.Error as e:
            self.logger.error(f"Error updating project: {e}")
            raise

    def delete_project(self, project_id: int) -> bool:
        """
        Delete a project from the database by ID.
        :param project_id: Integer ID of the project to delete
        :return: True if deleted successfully, False if not found
        """
        try:
            cursor = self.connection.cursor()
            result = cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            self.connection.commit()
            if result.rowcount == 0:
                self.logger.warning(f"Project {project_id} not found for deletion.")
                return False
            self.logger.info(f"Project {project_id} deleted.")
            return True
        except sqlite3.Error as e:
            self.logger.error(f"Error deleting project: {e}")
            raise

