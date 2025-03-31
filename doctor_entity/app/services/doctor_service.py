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
            # Extracting data from the request 
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            dept_name = data.get('department')
 
            # Validations
            if not first_name or not last_name or not dept_name:
                return {"error": "First name and last name and department are required"}, 400
           
            if not first_name.isalpha() or not last_name.isalpha():
                return {"error": "First name and last name must contain only letters"}, 400
            
            if not dept_name.isalpha():
                return{"error":"Department name must contain only letters"}, 400
            # Call repository function to insert doctor into the database
            doctor_id = self.doctor_repo.add_doctor(first_name, last_name, dept_name)
            
            # Return success response with doctor details
            return {"success": True, 
                    "doctor_id": doctor_id ,
                    "first_name":first_name,
                    "last_name":last_name, 
                    "department":dept_name}, 201
        
        # Handle unexpected errors and return a server error response
        # e is an object of Exception
        except Exception as e:
            return {"success": False,"error": str(e)}, 500
