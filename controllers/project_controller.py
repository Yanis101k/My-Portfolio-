import logging  # ✅ Used to log important backend operations
from typing import List, Optional  # ✅ Type hinting to make code clearer and safer
import sys  # ✅ Interact with the Python interpreter
import os   # ✅ Access OS-level functions (like path handling)

# ✅ Make root directory visible to Python so we can import modules from parent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.project import Project  # ✅ Data model representing a project
from database.project_dao import ProjectDAO  # ✅ DAO layer for DB interaction
from database.connector import DatabaseConnector  # ✅ Provides SQLite connection

class ProjectController:
    """
    ✅ Controller layer for managing project-related business logic.
    Acts as the intermediary between API routes and the DAO.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.dao = ProjectDAO(DatabaseConnector())

    def get_all_projects(self) -> List[Project]:
        """
        Fetch all projects from the database.
        :return: List of Project instances (empty list if none)
        """
        try:
            return self.dao.get_all_projects()
        except Exception as e:
            self.logger.error(f"Failed to get all projects: {e}")
            return []

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """
        Retrieve a single project by its ID.
        :param project_id: ID of the project to fetch
        :return: Project instance or None if not found
        """
        try:
            return self.dao.get_project_by_id(project_id)
        except Exception as e:
            self.logger.error(f"Error fetching project ID {project_id}: {e}")
            return None

    def create_project(self, data: dict) -> bool:
        """
        Create a new project using data provided as a dictionary.
        :param data: Dictionary with project fields
        :return: True if creation succeeded, else False
        """
        try:
            new_project = Project(
                id=None,
                title=data.get("title"),
                description=data.get("description"),
                image_url=data.get("image_url"),
                github_url=data.get("github_url"),
                live_url=data.get("live_url")
            )
            self.dao.add_project(new_project)
            self.logger.info(f"Created project: {new_project.get_title()}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating project: {e}")
            return False

    def update_project(self, project_id: int, data: dict) -> bool:
        """
        Update an existing project with given ID using a data dictionary.
        :param project_id: ID of the project to update
        :param data: Dictionary with updated fields
        :return: True if update succeeded, else False
        """
        try:
            updated_project = Project(
                id=project_id,
                title=data.get("title"),
                description=data.get("description"),
                image_url=data.get("image_url"),
                github_url=data.get("github_url"),
                live_url=data.get("live_url")
            )
            success = self.dao.update_project(updated_project)
            if success:
                self.logger.info(f"Updated project ID {project_id}")
            else:
                self.logger.warning(f"Project ID {project_id} not found for update")
            return success
        except Exception as e:
            self.logger.error(f"Error updating project {project_id}: {e}")
            return False

    def delete_project(self, project_id: int) -> bool:
        """
        Delete a project by its ID.
        :param project_id: ID of the project to delete
        :return: True if deletion succeeded, else False
        """
        try:
            success = self.dao.delete_project(project_id)
            if success:
                self.logger.info(f"Deleted project ID {project_id}")
            else:
                self.logger.warning(f"Project ID {project_id} not found for deletion")
            return success
        except Exception as e:
            self.logger.error(f"Error deleting project {project_id}: {e}")
            return False

