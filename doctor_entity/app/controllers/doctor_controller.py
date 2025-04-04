from flask import Blueprint, request, jsonify
from app.services.doctor_service import DoctorService
 
# Create a Blueprint for the Doctor route 
doctor_bp = Blueprint('doctor', __name__)

# Initialize the DoctorService instance to handle business logic
doctor_service = DoctorService()
 
class DoctorController:
    """
    Controller class for handling Doctor-related API requests
    """
    @staticmethod
    @doctor_bp.route('/doctor', methods=['POST'])
    def post_doctor():
        """
        Handles the POST request to create a new doctor.
        """
        data = request.get_json()
        response, status_code = doctor_service.create_doctor(data)
        return jsonify(response), status_code
