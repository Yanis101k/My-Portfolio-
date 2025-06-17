# middleware/api_key_required.py

from flask import request, jsonify
from functools import wraps
from config import Config

def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        client_key = request.headers.get('X-API-Key')
        if not client_key or client_key != Config.get_api_key():
            return jsonify({"error": "Unauthorized – Invalid or missing API key"}), 401
        return func(*args, **kwargs)
    return wrapper
