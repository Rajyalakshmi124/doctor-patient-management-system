import uuid
from flask import Blueprint, request, jsonify
from app.services.patient_services import PatientService
 
# Create a Blueprint for patient routes
patient_bp = Blueprint('patient', __name__) 

# Initialize PatientService
patient_service = PatientService()
 
class PatientController:
    # class for handling patient related API request
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
        # Handles fetching a patient by their ID.
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
        

    @staticmethod
    @patient_bp.route('/patient', methods=['GET'])
    def get_patient_by_name():
        # Handles fetching patients by their name (first name or full name).
        try:
            name = request.args.get('name', '').strip()
 
            # Validate name input
            if not name:
                return jsonify({"success": False, "errors": ["Patient name is required"]}), 400
            if not all(char.isalpha() or char.isspace() for char in name):
                return jsonify({"success": False, "errors": ["Name must contain only letters."]}), 400
 
            response = patient_service.get_patient_by_name(name)
            status_code = 200 if response["success"] else 404
            return jsonify(response), status_code
        except Exception as e:
            print(f"Error fetching patients by name: {e}")
            return jsonify({"success": False, "errors": [str(e)]}), 500


    @staticmethod
    @patient_bp.route('/patient/UnAssignDoctorFromPatient', methods=['POST'])
    def unassign_doctor_from_patient():
        try:
            # Get data from request
            data = request.get_json()
            doctor_id = data.get('doctorId', '').strip()
            patient_id = data.get('patientId', '').strip()

            # Initialize errors list to store validation errors
            errors = []

            # Validate if both doctor_id and patient_id are empty
            if not doctor_id and not patient_id:
                errors.append("Both Doctor ID and Patient ID are required")
            else:
                if not doctor_id:
                    errors.append("Doctor ID is required")
                if not patient_id:
                    errors.append("Patient ID is required")

            # Validate UUID format for doctor_id
            try:
                uuid.UUID(doctor_id)
            except ValueError:
                errors.append("Invalid doctorId format")

            # Validate UUID format for patient_id
            try:
                uuid.UUID(patient_id)
            except ValueError:
                errors.append("Invalid patientId format")

            # If there are errors, return them
            if errors:
                return jsonify({"success": False, "errors": errors}), 400

            # Call service method to unassign the doctor
            response, status_code = patient_service.unassign_doctor_from_patient(doctor_id, patient_id)

            return jsonify(response), status_code
        except Exception as e:
            return jsonify({"success": False, "errors": [str(e)]}), 500
