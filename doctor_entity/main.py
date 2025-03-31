from flask import Flask
from app.controllers.patient_controller import patient_bp
 
# Initialize Flask App
app = Flask(__name__)
 
# Register Blueprints
app.register_blueprint(patient_bp)
 
if __name__ == '__main__':
    app.run(debug=True)
