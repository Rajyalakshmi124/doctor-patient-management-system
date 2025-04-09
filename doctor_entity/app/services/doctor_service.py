from app.repositories.doctor_repository import DoctorRepository
import uuid
 
class DoctorService:
    def __init__(self):
        # Initialize the DoctorRepository instance to interact with database
        self.doctor_repo = DoctorRepository()
 
    def create_doctor(self, data):
        """
        Handles doctor creation with validations.
        """
       
        try:
            # Extracting data from the request JSON 
            firstName = data.get('firstName')
            lastName = data.get('lastName')
            department = data.get('department')
 
            # Validations
            errors = [] 
            if not firstName or not firstName.strip():
                errors.append("First name is required")
            else:
                firstName = firstName.strip()
            if not all(char.isalpha() or char.isspace() for char in firstName):
                errors.append("First name must contain only letters and spaces")

            # Validates Last Name
            if not lastName or not lastName.strip:
                errors.append("Last name is required")
            else:
                lastName = lastName.strip()
            if not all(char.isalpha() or char.isspace() for char in lastName):
                errors.append("Last name must contain only letters and spaces")

            # Validates Department Name
            if not department or not department.strip:
                errors.append("Department name are required"), 400
            else:
                department = department.strip()
            if any(char.isdigit() for char in department):
                errors.append("Department name must contain only alphabets,spaces and special symbolls"), 400

            if errors:
                return {"success": False, "errors": errors},400
            
            # Ensure no additional fields are present in the input data
            if len(data) > 3:
                return {"success": False, "errors": ["Only first name and last name and department are allowed"]}, 400
            
            # Call repository function to insert doctor into the database
            doctor_id = self.doctor_repo.add_doctor(firstName, lastName, department)
            
            # Return success response with doctor details
            return { 
                    "success": True, 
                    "id": doctor_id ,
                    "firstName":firstName,

                    "lastName":lastName, 
                    "department":department
            }, 200
        
        # Handle unexpected errors and return a server error response
        # e is an object of Exception
        except Exception as e:
            return {"success": False,"errors": [str(e)]}, 500
        
    def get_doctor_details(self, doctor_id):
        try:
            if not doctor_id or not doctor_id.strip():
                return {"success": False, "errors": ["Doctor ID is required"]}, 400

            # Validate if the doctor_id is a valid UUID
            try:
                uuid.UUID(doctor_id)
            except ValueError:
                return {"success": False, "errors": ["Invalid Doctor ID format"]}, 400

            doctor = self.doctor_repo.get_doctor_by_id(doctor_id)
            if not doctor:
                return {"success": False, "errors": ["Doctor not found"]}, 404

            return {
                "success": True,
                "id": doctor["id"],
                "firstName": doctor["firstName"],
                "lastName": doctor["lastName"],
                "department": doctor["department"]
            }, 200
        
        # Handle unexpected errors and return a server error response
        # e is an object of Exception
        except Exception as e:
            return {"success": False, "errors": [str(e)]}, 500
