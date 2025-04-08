from flask import Blueprint, request, jsonify
from app.services.patient_sevices import PatientService
 
# Create a Blueprint for patient routes
patient_bp = Blueprint('patient', __name__) 

# Initialize PatientService
patient_service = PatientService()
 
class PatientController:
    """
    class for handling patient related API request
    """
    @staticmethod
    @patient_bp.route('/patient', methods=['POST'])
    def post_patient():
        """Handles the creation of a new patient."""
        try:
            data = request.get_json()
 
            if not data:
                return jsonify({"success": False, "errors": ["Request body must be JSON."]}), 400
 
            response, status_code = patient_service.create_patient(data)
            return jsonify(response), status_code
 
        except Exception as e:
            return jsonify({"success": False, "errors": [str(e)]}), 500


    @staticmethod
    @patient_bp.route('/patient/<patient_id>', methods=['GET'])
    def get_patient(patient_id):
        """Handles fetching a patient by their ID."""
        try:
            patient_id=int(patient_id)
            # Validate patient_id
            if (not patient_id) or (patient_id <= 0):
                return jsonify({"success": False, "errors": ["Invalid patient ID"]}), 400
            
            response = patient_service.get_patient_by_id(patient_id)
            status_code = 200 if response["success"] else 404
            return jsonify(response), status_code
        except ValueError:
            return jsonify({"success": False, "errors": ["Patient ID should be an integer"]}),400  
        except Exception as e:
            # Print the exception for debugging purposes
            print(f"Error fetching patient: {e}")
            return jsonify({"success": False, "errors": [str(e)]}), 500
