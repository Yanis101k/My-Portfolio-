import sqlite3 # Built-in Python module to interact with SQLite databases 
import logging # Used to log messages for debugging and monitoring 

#The sys module allows you to interact with the Python interpreter itself. It's useful for handling system-specific information 
# and controlling the program's behavior.
# Add path for module search
import sys

#The os module in Python gives you access to operating system features like : 
#reading or writing files, navigating folders, and managing environment variables.
import os


# Make root directory visible to Python so we can import project.py model
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Project Model that we will work with 
from models.project import Project 

# Import the DatabaseConnector class to get a database connection 
from database.connector import DatabaseConnector 

class ProjectDAO:
       """
       DAO (Data Access Object ) class for handling all database operations ( crud ) 
       related to Project entities. Follows clean separation of concern by 
       keeping SQL logic out of the business logic ( Controller/Model )
       """ 

       def __init__( self , db_connector: DatabaseConnector ): 
              """
              Constructor : Initialize the DAO with an existing database connection .
              :param db_connector : An instance of DatabaseConnector class  
              """ 

              self.logger = logging.getLogger(__name__) # set_up logger specific to this class 
              self.connection = db_connector.connect() # using the existing connection from the connector 
        
       def get_all_projects(self):
              """
              Retrieves all projects from database.
              :return: List of Project objects   
              """ 

              try: 
                     cursor = self.connection.cursor() # Create a cursor to execute SQL 
                     cursor.execute("SELECT * FROM projects") # Retrieve all rows from the projects table 
                     rows = cursor.fetchall() # Fetch as list of tuples
                     projects = []

                     for row in rows : 
                      # Convert each tuple into a Project object using the unpacking operator
                      project = Project(*row)
                      projects.append(project)
                    
                     self.logger.info(f"{len(projects)} projects fetched from the database ")
                     return projects 
              except sqlite3.Error as e : 
                    # Log the error and raise it again to notify the calling code 
                    self.logger.error(f"Error fetching projects: {e}")
                    raise 
       

       def get_project_by_id( self , project_id ) : 
             """
             retrives a single project by its unique ID 
             :param project_id: Integer ID of the project 
             :return: A Project Object or None if not found 
             """ 
             try:
                cursor = self.connection.cursor() # Create a cursor to execute SQL   
                cursor.execute( "SELECT * FROM projects WHERE id = ? " , ( project_id ,) )
                row = cursor.fetchone()
                if row : 
                        project = Project(*row)
                        self.logger.info(f"Project {project_id} found. ")
                        return project 
                else : 
                        self.logger.warning(f"Project {project_id} not found ")
             except sqlite3.Error as e :
                self.logger.error(f"Error fetching project by ID : {e}") 
        

       def add_project( self , project : Project ) : 
            """
            Insert new project record to database.
            :param project: An instance of the project model  
            """ 

            try :
                  cursor = self.connection.cursor()
                  # Insert new row using the data from Project instance 
                  cursor.execute(""" 
                     INSERT INTO projects ( title , description , image_url , github_url , live_url )
                     VALUES (? , ? , ? , ? , ? )""", (
                     project.get_title() , 
                     project.get_description() , 
                     project.get_image_url() , 
                     project.get_github_url() , 
                     project.get_live_url()
                                 )) 
                  self.connection.commit() # save changes to the database
                  self.logger.info("New Project Inserted successfully. ")

            except sqlite3.Error as e : 
                  self.logger.error(f"Error Inserting project : {e}")
                  raise 

       def update_project(self, project: Project):
        """
        Updates an existing project’s information.
        :param project: An updated Project object (must include its ID)
        """
        try:
            cursor = self.connection.cursor()

            # ✅ Update row where ID matches
            cursor.execute("""
                UPDATE projects
                SET title = ?, description = ?, image_url = ?, github_url = ?, live_url = ?
                WHERE id = ?
            """, (
                project.get_title(),
                project.get_description(),
                project.get_image_url(),
                project.get_github_url(),
                project.get_live_url(),
                project.get_id()
            ))

            self.connection.commit()
            self.logger.info(f"Project {project.get_id()} updated.")
        except sqlite3.Error as e:
            self.logger.error(f"Error updating project: {e}")
            raise

       def delete_project( self , project_id ) :
             """
             Delet Project from the databse using ID . 
             :param project_id: Integer ID of the project to delete 
             """

             try : 
                   
                   cursor = self.connection.cursor()
                   cursor.execute("DELETE FROM projects WHERE id = ? " , (project_id ,))
                   self.connection.commit() # save changes to the database 
                   self.logger.info( f"Project {project_id} deleted.")
             
             except sqlite3.Error as e :
                   self.logger.error(f"Error deleting project : {e}")
                   raise 
  
