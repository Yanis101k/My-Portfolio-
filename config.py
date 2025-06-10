import os 
from dotenv import load_dotenv

# Load environement variables from the .env file 
load_dotenv()

# Define a config class that holds all config variables 
class Config : 

    # static and private attributes to represent the environment variables 
    
    # Flask secret key ( used for sessions , CSRF , etc ..)
    __SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

    # Admin credentials ( used for admin authentication )
    __ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    __ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")

    # Path to the database 
    __DATABASE_PATH = os.getenv("DATABASE_PATH" , "database/portfolio.db")

    # Logging configuration 
    __LOG_FILE = os.getenv("LOG_FILE" , "logs/app.log")

    # App environment settings 
    __DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"
    
    # static getters to access those environment variables 
    @staticmethod
    def get_secret_key( ) : 
        return Config.__SECRET_KEY 
    
    @staticmethod
    def get_admin_username( ) : 
        return Config.__ADMIN_USERNAME
    
    @staticmethod
    def get_admin_password_hash( ) : 
        return Config.__ADMIN_PASSWORD_HASH
    
    @staticmethod
    def get_database_path(  ) : 
        return Config.__DATABASE_PATH  
    
    @staticmethod
    def get_log_file( ) : 
        return Config.__LOG_FILE
    
    @staticmethod
    def get_debug( ) : 
        return Config.__DEBUG

