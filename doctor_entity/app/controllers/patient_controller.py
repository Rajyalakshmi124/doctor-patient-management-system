from flask import Blueprint, request, jsonify
from app.services.doctor_service import DoctorService
from app.services.patient_services import PatientService
from app.dual_auth import dual_auth 
 
# Create a Blueprint for patient routes
patient_bp = Blueprint('patient', __name__)
 
# Initialize PatientService
patient_service = PatientService()
doctor_service = DoctorService()
 
class PatientController:
    # class for handling patient related API request
    @staticmethod
    @patient_bp.route('/patient', methods=['POST'])
    @dual_auth
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
    @dual_auth
    def get_patient(patient_id):
        # Handles fetching a patient by their ID.
        try:
            # Validate patient_id
            if not patient_id or not patient_id.strip():
                return jsonify({"success": False, "errors": ["Patient ID is required"]}), 400
           
            # Validate if the patient_id is a valid UUID
            if not doctor_service._valid_uuid(patient_id):
                return{"success":False, "errors":["Invalid Patient ID format"]}, 400
 
            response = patient_service.get_patient_by_id(patient_id)
            status_code = 200 if response["success"] else 404
            return jsonify(response), status_code
        except Exception as e:
            # Print the exception for debugging purposes
            print(f"Error fetching patient: {e}")
            return jsonify({"success": False, "errors": [str(e)]}), 500

    @staticmethod
    @patient_bp.route('/patient', methods=['GET'])
    @dual_auth
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
    @patient_bp.route('/UnAssignDoctorFromPatient', methods=['POST'])
    @dual_auth
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
 
            # If there are errors, return them
            if errors:
                return jsonify({"success": False, "errors": errors}), 400
 
            # Validate if the doctor_id is a valid UUID
            if not doctor_service._valid_uuid(doctor_id):
                return{"success":False, "error":["Invalid Doctor ID format"]}, 400
 
            # Validate if the patient_id is a valid UUID
            if not doctor_service._valid_uuid(patient_id):
                return{"success":False, "error":["Invalid Patient ID format"]}, 400
 
            # Call service method to unassign the doctor
            response, status_code = patient_service.unassign_doctor_from_patient(doctor_id, patient_id)
 
            return jsonify(response), status_code
        except Exception as e:
            return jsonify({"success": False, "errors": [str(e)]}), 500

    @staticmethod
    @patient_bp.route('/patientsByDoctorId', methods=['GET'])
    @dual_auth
    def get_patients_by_doctor_id():
        try:
            doctor_id = request.args.get('doctorId', '').strip()
            if not doctor_id:
                return jsonify({"success": False, "errors": ["DoctorId is required"]}), 400
   
            # Validate if the doctor_id is a valid UUID
            if not doctor_service._valid_uuid(doctor_id):
                return{"success":False, "error":["Invalid Doctor ID format"]}, 400
   
            response, status_code = patient_service.get_patients_by_doctor_id(doctor_id)
            return jsonify(response), status_code
        except Exception as e:
            return jsonify({"success": False, "errors": [str(e)]}), 500
 
    # PATCH /patient/{patientId} - Update patient details
    @staticmethod
    @patient_bp.route('/patient/<patient_id>', methods=['PATCH'])
    @dual_auth
    def update_patient(patient_id):
        try:
            patient_id=patient_id.strip()
            # Validate patient_id
            if not patient_id:
                return jsonify({"success": False, "errors": ["Patient ID is required"]}), 400
           
            # Validate patient_id format
            if not doctor_service._valid_uuid(patient_id):
                return jsonify({"success": False, "errors": ["Invalid Patient ID format"]}), 400
   
            # Get data from request
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "errors": ["Request body must be JSON."]}), 400
   
            # Call service method to update patient details
            response, status_code = patient_service.update_patient_by_id(patient_id, data)
            return jsonify(response), status_code
   
        except Exception as e:
            return jsonify({"success": False, "errors": [str(e)]}), 500
 
    # DELETE /patient/{patientId} - Delete patient
    @staticmethod
    @patient_bp.route('/patient/<patient_id>', methods=['DELETE'])
    @dual_auth
    def delete_patient(patient_id):
        # Handles deleting a patient.
        try:
            patient_id=patient_id.strip()
            # Validate patient_id
            if not patient_id:
                return jsonify({"success": False, "errors": ["Patient ID is required"]}), 400
           
            # Validate patient_id format
            if not doctor_service._valid_uuid(patient_id):
                return{"success":False, "error":["Invalid Patient ID format"]}, 400
   
            # Call service method to check and delete the patient
            response, status_code = patient_service.delete_patient_by_id(patient_id)
            return jsonify(response), status_code
   
        except Exception as e:
            return jsonify({"success": False, "errors": [str(e)]}), 500
