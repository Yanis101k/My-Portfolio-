
from functools import wraps 
from flask import jsonify
from flask import session
import logging
logger = logging.getLogger(__name__)


def login_required(f):
    @wraps (f)
    def wrapper(*args , **kwargs ):
         
         if "username" not in session:
              logger.warning("Unauthorized access attempt to a protected route")
              return jsonify({"error":"Unauthrized"}) , 401 
         return f(*args , **kwargs )
        
    return wrapper


