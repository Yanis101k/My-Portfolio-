# test_config.py
import sys
import os

# Make root directory visible to Python so we can import config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the Config class from config.py to access app settings
from config import Config

# Print each config variable to confirm it's loaded correctly from .env
def test_print_config():
    print("Testing config loading...\n")
    print("SECRET_KEY:", Config.SECRET_KEY)
    print("ADMIN_USERNAME:", Config.ADMIN_USERNAME)
    print("ADMIN_PASSWORD_HASH:", Config.ADMIN_PASSWORD_HASH)
    print("DATABASE_PATH:", Config.DATABASE_PATH)
    print("DEBUG:", Config.DEBUG)
    print("LOG_FILE:", Config.LOG_FILE)


if __name__ == "__main__":
    test_print_config()
