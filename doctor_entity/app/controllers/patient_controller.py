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
