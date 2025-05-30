# test_config.py
import sys
import os

# Make root directory visible to Python so we can import config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.generate_password_hash 

def print_hashed_password() : 

    # Prompt the user to input the admin password and encode it in UTF-8 format.
    password = input("Enter your admin password: ")
    # Print a message to indicate where the user should copy the result.
    print("Hash to copy into .env:")


    print(utils.generate_password_hash.get_hashed_password( password ))