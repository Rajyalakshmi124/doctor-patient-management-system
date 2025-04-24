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
            allowed_feilds=['firstName','lastName']
            if any(field not in allowed_feilds for field in data.keys()):
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
            return {"success": False, "errors": [e]}, 500
        
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
        
    def get_patient_by_name(self, name):
        #Fetches patients by their full or partial name (first name or last name).
        try:
            name_parts = name.strip().split()
 
            # Split the full name into first and last name (if possible)
            if len(name_parts) == 2:
                first_name, last_name = name_parts
            else:
                first_name = name_parts[0]
                last_name = None
 
            # Call repository function to fetch patients by name
            patients = self.patient_repo.get_patient_by_name_combined(first_name, last_name)
 
            if not patients:
                return {"success": False, "errors": ["Patient not found"]}

 
            return {
                "success": True,
                "patients": patients
            }
        except Exception as e:
            return {"success": False, "errors": [str(e)]}, 500

    def unassign_doctor_from_patient(self, doctor_id, patient_id):
        try:
            
            result = self.patient_repo.remove_doctor_assignment(doctor_id, patient_id)
            if not result:
                return {"success": False, "errors": ["No matching assignment found"]}, 400
    
            return {"success": True}, 200
    
        except Exception as e:
            return {"success": False, "errors": [str(e)]}, 500

    def get_patients_by_doctor_id(self, doctor_id):
        try:
            # Validate UUID here if needed (already done in controller)
            doctor, patients = self.patient_repo.get_patients_by_doctor_id(doctor_id)

            if not doctor:
                return {"success": False, "errors": ["Doctor has no assigned patients"]}, 404

            return {
                "success": True,
                "doctor": doctor,
                "patients": patients
            }, 200
        except Exception as e:
            return {"success": False, "errors": [str(e)]}, 500
