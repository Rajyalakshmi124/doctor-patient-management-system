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
            
            # Ensure no additional fields are present in the input data
            if len(data) > 2:
                return {"success": False, "errors": ["Only first name and last name are allowed"]}, 400

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
        

    def get_patient_by_id(self, patient_id):
        try:
            # Fetch the patient from the repository by ID
            patient = self.patient_repo.get_patient_by_id(patient_id)
            if not patient:
                return {"success": False, "errors": ["Patient not found"]}
            
            return {
                "success": True,
                "id": patient["id"],
                "firstName": patient["firstName"],
                "lastName": patient["lastName"]
            }
        except Exception as e:
            return {"success": False, "errors": [str(e)]}