from flask import Blueprint, request , session , jsonify
import logging


# the sys module allow us to interact with the Python interpreter . it's useful for handling system-specific information
#and controlling the program's behavior 
#Add path for module search 
import sys 

# the os module in python gives you access to operating system features like : 
# reading or writing files , navigating folders , and managing environment variables.
# Used to set environment variables during testing 

import os 

#  Make root directory visible to python se we can import config.py
sys.path.append( os.path.abspath( os.path.join( os.path.dirname(__file__) , '..' )))

from config import Config
from utils.hashing import Hashing 

api_auth = Blueprint( "api_auth", __name__ )
logger = logging.getLogger(__name__) 
from middleware.api_key_required import require_api_key

@api_auth.route("/api/login" , methods=["POST"])
@require_api_key
def login():
    
    try:
        # ✅ Ensure it's a valid JSON request
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request must be in JSON format"}), 400

        # ✅ Extract and validate input fields
       
        username = data.get("username")
        password = data.get("password")

        # ✅ Check for missing fields
        if username is None or password is None:
            return jsonify({"error": "Username and password are required"}), 400

        # ✅ Check type and non-empty strings
        if not isinstance(username, str) or not isinstance(password, str):
            return jsonify({"error": "Username and password must be strings"}), 400

        if username.strip() == "" or password.strip() == "":
            return jsonify({"error": "Username and password cannot be empty"}), 400

        # ✅ Validate against stored admin credentials
        
        if username.strip() == Config.get_admin_username() and Hashing.check_password( password.strip() , Config.get_admin_password_hash()):
            session["username"] = username
            logger.info(f"User '{username}' successfully logged in")
            return jsonify({"message": "Login successful"}), 200

        logger.warning(f"Failed login attempt for username: {Config.get_admin_username()} ")
        return jsonify({"error": "Invalid username or password"}), 401

    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"error": "Something went wrong"}), 500
        
@api_auth.route("/api/logout" , methods=["POST"])
@require_api_key
def logout():

    user = session.get("username", "unknown")
    session.clear()
    logger.info(f"User '{user}' logged out")
    return jsonify({"message" : "Logged out successfully" }) , 200
