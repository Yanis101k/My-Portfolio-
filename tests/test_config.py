# test_config.py
#The sys module allows you to interact with the Python interpreter itself. It's useful for handling system-specific information 
# and controlling the program's behavior.
# Add path for module search
import sys

#The os module in Python gives you access to operating system features like : 
#reading or writing files, navigating folders, and managing environment variables.
import os

# Make root directory visible to Python so we can import config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load .env.test before importing Config or app
from dotenv import load_dotenv
env_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '.env.test')
load_dotenv(dotenv_path=env_path)
# Import the Config class from config.py to access app settings
from config import Config

# Print each config variable to confirm it's loaded correctly from .env
def test_print_config():
    print("Testing config loading...\n")
    print("SECRET_KEY:", Config.get_secret_key() )
    print("ADMIN_USERNAME:", Config.get_admin_username())
    print("ADMIN_PASSWORD_HASH:", Config.get_admin_password_hash() )
    print("DATABASE_PATH:", Config.get_database_path() )
    print("DEBUG:", Config.get_debug())

if __name__ == "__main__":
    test_print_config()
