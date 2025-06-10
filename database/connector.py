import sqlite3 # Standard Python module to connect and interact with sqlite datbases 
import logging # Used to log info , warnings , and errors during DB operations

#The sys module allows you to interact with the Python interpreter itself. It's useful for handling system-specific information 
# and controlling the program's behavior.
# Add path for module search
import sys

#The os module in Python gives you access to operating system features like : 
#reading or writing files, navigating folders, and managing environment variables.
import os


# Make root directory visible to Python so we can import project.py model
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config # loads environement-based config values such DB path 

class DatabaseConnector:
    """
    A class to manage the connection to the SQLite database using best practices.
    It uses encapsulation to protect internal state and exposes safe access methods.
    """

    def __init__(self):
        # initialize logger 
        self.logger = logging.getLogger(__name__)

        # Private Attribute for database path 
        self.__db_path= Config.get_database_path()

        # Private attribute to hold the SQLite connection 

        self.__connection = None 
    
    """
     Check if the app is currently connected to the database.
    :return: True if connection is active, False otherwise.
    """
    def app_connected_to_database( self ) -> bool :
         
         connected = self.__connection is not None 
         self.logger.info(f" database connection check : {connected} ") 
         return connected    


    def connect( self ):

        """
        Establish a connection to the SQLite database
        """

        if self.__connection : 
             # if the application is connected before we don't need to connect again
             return self.__connection 
        else : 
                try:
                    self.__connection = sqlite3.connect(self.__db_path)
                    self.logger.info(f"Connected to database : {self.__db_path}")
                    return self.__connection
            
                except sqlite3.Error as e : 
                    self.logger.error(f"Failed to connect database : {e}")
                    raise 
            
    def close( self ) : 

            """
            Closes the database connection safely.
            """

            if( self.__connection ) : 
                self.__connection.close()
                self.logger.info("Database connection closed. ")
                self.__connection = None 