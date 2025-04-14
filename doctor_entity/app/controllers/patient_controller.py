import uuid
from flask import Blueprint, request, jsonify
from doctor_entity.app.services.patient_services import PatientService
 
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
            # Validate patient_id
            if not patient_id or not patient_id.strip():
                return jsonify({"success": False, "errors": ["Patient ID is required"]}), 400
            
            # Check if patient_id is a valid UUID
            try:
                uuid.UUID(patient_id)
            except ValueError:
                return jsonify({"success": False, "errors": ["Invalid Patient ID format"]}), 400

            response = patient_service.get_patient_by_id(patient_id)
            status_code = 200 if response["success"] else 404
            return jsonify(response), status_code
        except Exception as e:
            # Print the exception for debugging purposes
            print(f"Error fetching patient: {e}")
            return jsonify({"success": False, "errors": [str(e)]}), 500
