import os 
from dotenv import load_dotenv

# Load environement variables from the .env file 
load_dotenv()

# Define a config class that holds all config variables 
class Config : 

    # Flask secret key ( used for sessions , CSRF , etc ..)
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

    # Admin credentials ( used for admin authentication )
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")

    # Path to the database 
    DATABASE_PATH = os.getenv("DATABASE_PATH" , "database/portfolio.db")

    # Logging configuration 
    LOG_FILE = os.getenv("LOG_FILE" , "logs/app.log")

    # App environment settings 
    DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"