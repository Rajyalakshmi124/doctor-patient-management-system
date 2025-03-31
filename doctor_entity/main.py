from flask import Flask
from app.controllers.doctor_controller import doctor_bp
 
# Initialize Flask App
app = Flask(__name__)
 
# Register Blueprints
app.register_blueprint(doctor_bp)
 
if __name__ == '__main__':
    app.run(debug=True)