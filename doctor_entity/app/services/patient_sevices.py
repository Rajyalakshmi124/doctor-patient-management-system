from app.repositories.patient_repository import PatientRepository

class PatientService:
    def __init__(self):
        self.patient_repo = PatientRepository()

    def create_patient(self, data):
        # Handles patient creation with validation.
        try:
            # Extracting data
            first_name = data.get('first_name')
            last_name = data.get('last_name')

            # Validation
            errors = []
            if not first_name or not last_name:
                errors.append("First name and last name are required")
            
            if not first_name.isalpha() or not last_name.isalpha():
                errors.append("First name and last name must contain only letters")

            if errors:
                return {"success": False, "errors": errors}, 400

            # Call repository to save patient
            patient_id = self.patient_repo.add_patient(first_name, last_name)

            return {
                "success": "True",
                "id": patient_id,
                "firstName": first_name,
                "lastName": last_name
            }, 201
        
        except Exception as e:
            return {"success": "False", "errors": [str(e)]}, 500
        