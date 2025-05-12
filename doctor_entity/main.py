from flask import Flask, jsonify
from flask_oidc import OpenIDConnect
from app.controllers.patient_controller import patient_bp
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.json.sort_keys = False

# OIDC Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['OIDC_CLIENT_SECRETS'] = os.getenv('OIDC_CLIENT_SECRETS')
app.config['OIDC_SCOPES'] = ['openid', 'email']
app.config['OIDC_RESOURCE_SERVER_ONLY'] = True
app.config['OIDC_INTROSPECTION_AUTH_METHOD'] = 'client_secret_post'

# Initialize OIDC
oidc = OpenIDConnect(app)

# Register Blueprints
app.register_blueprint(patient_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
