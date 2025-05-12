from functools import wraps
from flask import request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from dotenv import load_dotenv
import os
 
# Load environment variables from .env file
load_dotenv()
 
# Your Google Client ID from environment variable
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
 
# Decorator to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')
       
        # Check if the header is missing or doesn't start with "Bearer "
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing"}), 401
       
        # Extract the token from the header
        token = auth_header.split(" ")[1]
       
        try:
            # Verify the token with Google's OAuth2 service
            id_info = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
           
            # Check if the email is verified
            if not id_info.get("email_verified"):
                return jsonify({"error": "Email not verified"}), 403
       
        except ValueError:
            # Handle invalid token
            return jsonify({"error": "Invalid token"}), 401
       
        # Call the original function if everything is fine
        return f(*args, **kwargs)
   
    return decorated_function