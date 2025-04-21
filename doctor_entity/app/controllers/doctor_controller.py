from flask import Blueprint, request, jsonify
from app.services.doctor_service import DoctorService
 
# Create a Blueprint for the Doctor route 
doctor_bp = Blueprint('doctor', __name__)

# Initialize the DoctorService instance to handle business logic
doctor_service = DoctorService()

# Controller class for handling Doctor-related API requests.
class DoctorController:

    @staticmethod
    @doctor_bp.route('/doctor', methods=['POST'])
    # Handles the POST request to create a new doctor.
    def post_doctor():
        data = request.get_json()
        response, status_code = doctor_service.create_doctor(data)
        return jsonify(response), status_code
    
    @staticmethod
    @doctor_bp.route('/doctor/<doctor_id>', methods=['GET'])
    # Handles the GET request to fetch a doctor by ID.
    def get_doctor(doctor_id):
        response, status_code = doctor_service.get_doctor_details(doctor_id)
        return jsonify(response), status_code
    
    @staticmethod
    @doctor_bp.route('/doctor', methods=['GET'])
    # Handles the GET request to search doctor by first name or last name.
    def search_doctors():
        name = request.args.get('name', '')
        response, status_code = doctor_service.search_doctors_by_name(name)
        return jsonify(response), status_code
    
    @staticmethod
    @doctor_bp.route('/AssignDoctorToPatient', methods=['POST'])
    def assign_doctor_to_patient():
    # Handles the POST request to assign a doctor to a patient
        data = request.get_json()
        response,status_code = doctor_service.assign_doctor_to_patient(data)
        return jsonify(response), status_code
