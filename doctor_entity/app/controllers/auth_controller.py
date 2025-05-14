from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

# Defining a blueprint for authentication routes.
auth_bp = Blueprint('auth', __name__)
 
# It stores for registered users and active tokens
users = {}
active_tokens = {}
 
# Route to register a new user
@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

 # Validations
    if not username or not password:
        return jsonify({"success": False, "error": "Username and password required"}), 400
 
    if username in users:
        return jsonify({"success": False, "error": "User already exists"}), 400
 
    users[username] = password
    return jsonify({"success": True, "message": "User registered successfully"}), 201
 
# Route to login an existing user
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Validations
    if not username or not password:
        return jsonify({"success": False, "error": "Username and password required"}), 400
 
    if username not in users or users[username] != password:
        return jsonify({"success": False, "error": "Invalid credentials"}), 401
 
    if username in active_tokens:
        return jsonify({"success": False, "error": f"User '{username}' is already logged in"}), 403
 
    # Generate and store access token
    token = create_access_token(identity=username)
    active_tokens[username] = token
    return jsonify({"success": True, "token": token}), 200
