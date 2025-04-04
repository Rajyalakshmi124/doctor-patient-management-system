from app.repositories.doctor_repository import DoctorRepository
 
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
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            dept_name = data.get('department')
 
            # Validations
            errors = [] 
            if not first_name or not first_name.strip():
                errors.append("First name is required")
            else:
                first_name = first_name.strip()
            if not all(char.isalpha() or char.isspace() for char in first_name):
                errors.append("First name must contain only letters and spaces")

            # Validates Last Name
            if not last_name or not last_name.strip:
                errors.append("Last name is required")
            else:
                last_name = last_name.strip()
            if not all(char.isalpha() or char.isspace() for char in last_name):
                errors.append("Last name must contain only letters and spaces")

            # Validates Department Name
            if not dept_name or not dept_name.strip:
                errors.append("Department name are required"), 400
            else:
                dept_name = dept_name.strip()
            if any(char.isdigit() for char in dept_name):
                errors.append("Department name must contain only alphabets,spaces and special symbolls"), 400

            if errors:
                return {"success": False, "errors": errors},400
            
            # Call repository function to insert doctor into the database
            doctor_id = self.doctor_repo.add_doctor(first_name, last_name, dept_name)
            
            # Return success response with doctor details
            return { 
                    "success": True, 
                    "id": doctor_id ,
                    "firstName":first_name,
                    "lastName":last_name, 
                    "department":dept_name
            }, 201
        
        # Handle unexpected errors and return a server error response
        # e is an object of Exception
        except Exception as e:
            return {"success": False,"errors": [str(e)]}, 500
