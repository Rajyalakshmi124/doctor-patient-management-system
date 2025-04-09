from flask import Flask 
from app.controllers.doctor_controller import doctor_bp
from app.controllers.patient_controller import patient_bp

app = Flask(__name__) 
app.json.sort_keys = False
  
# Pass the required route to the decorators
app.register_blueprint(doctor_bp)
app.register_blueprint(patient_bp)
  
if __name__ == "__main__": 
    app.run(debug=True)
 