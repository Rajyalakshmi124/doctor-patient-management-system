from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

def dual_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing or invalid"}), 401

        token = auth_header.split(" ")[1]

        # Try JWT verification
        try:
            verify_jwt_in_request()
            identity = get_jwt_identity()
            request.user_identity = identity
            return f(*args, **kwargs)
        except Exception:
            # JWT failed, try OpenID next
            pass  

        # Try Google OpenID verification
        try:
            id_info = id_token.verify_oauth2_token(token, google_requests.Request())
            if not id_info.get("email_verified"):
                return jsonify({"error": "Email not verified"}), 403

            request.user_identity = id_info["email"]
            return f(*args, **kwargs)
        except Exception:
            return jsonify({"error": "Invalid or expired token"}), 401

    return decorated_function
