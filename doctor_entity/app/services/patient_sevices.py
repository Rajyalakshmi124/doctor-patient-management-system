from app.repositories.patient_repository import PatientRepository

class PatientService:
    def __init__(self):
        # Initialize the PatientRepository instance to interact with the database
        self.patient_repo = PatientRepository()

    def create_patient(self, data):
        try:
            # Extract and strip first and last names from the input data
            firstName = data.get('firstName', '').strip()
            lastName = data.get('lastName', '').strip()

            # Initialize an empty list to collect validation errors
            errors = []
            if not firstName or not lastName:
                errors.append("First name and last name are required")
            if not firstName.replace(' ', '').isalpha():
                errors.append("First name must contain only letters and spaces")
            if not lastName.replace(' ', '').isalpha():
                errors.append("Last name must contain only letters and spaces")

            # If there are validation errors, return them with a 400 status code
            if errors:
                return {"success": False, "errors": errors}, 400

            # Add the patient to the repository and get the patient ID
            patient_id = self.patient_repo.add_patient(firstName, lastName)
            
            # Return success response with patient details
            return {"success": True, 
                    "id": patient_id, 
                    "firstName": firstName, 
                    "lastName": lastName
                    }, 201

        except Exception as e:
            # Handle unexpected errors and return a server error response
            return {"success": False, "errors": [str(e)]}, 500
