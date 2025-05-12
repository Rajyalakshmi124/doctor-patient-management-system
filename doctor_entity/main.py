import os
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from app.controllers.doctor_controller import doctor_bp
from app.controllers.patient_controller import patient_bp
from app.controllers.auth_controller import auth_bp

# Load environment variables from a .env file
load_dotenv()

# Initialize the flask application
app = Flask(__name__) 
app.json.sort_keys = False

# JWT Configuration using secret key from environment
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)
  
# Pass the required route to the decorators
app.register_blueprint(doctor_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(auth_bp)

# Start the flask application
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8000)
