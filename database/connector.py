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
        self.__db_path= Config.DATABASE_PATH

        # Private attribute to hold the SQLite connection 

        self.__connection = None 

    
    def __connect( self ):

        """
        Establish a connection to the SQLite database
        using private methode because this methode 
        will be never used outside this class and 
        the external classes will use get_connection methode 
        to connect to the datbase ( encapusation priciple applied ) 
        """

        try:
            self.__connection = sqlite3.connect(self.__db_path)
            self.logger.info(f"Connected to database : {self.__db_path}")
        except sqlite3.Error as e : 
            self.logger.error(f"Failed to connect database : {e}")
            raise

    def get_connection( self ) : 
            
            """
            Returns the active connection , connecting if necessary.
            """
            if self.__connection is None: 
                self.__connect()
            return self.__connection 
        

    def close( self ) : 

            """
            Closes the database connection safely.
            """

            if( self.__connection ) : 
                self.__connection.close()
                self.logger.info("Database connection closed. ")
                self.__connection = None 