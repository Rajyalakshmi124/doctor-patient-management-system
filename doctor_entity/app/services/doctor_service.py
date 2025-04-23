from app.repositories.doctor_repository import DoctorRepository
import uuid
from datetime import datetime
 
class DoctorService:
    def __init__(self):
        # Initialize the DoctorRepository instance to interact with database
        self.doctor_repo = DoctorRepository()

    # Reusable method to validate UUID format.
    def _valid_uuid(self, value):
        try:
            uuid.UUID(value)
            return True
        except ValueError:
            return False

# Handles doctor creation with validations. 
    def create_doctor(self, data):
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
            feilds=["firstName","lastName","department"]
            if any(field not in feilds for field in data.keys()):
                return {"success": False, 
                        "errors": ["Only first name, last name and department are allowed"]
                }, 400
            
            # Call repository function to insert doctor into the database
            doctor_id = self.doctor_repo.add_doctor(firstName, lastName, department)
            
            # Return success response with doctor details
            return { 
                    "success": True, 
                    "id": doctor_id ,
                    "firstName":firstName,
                    "lastName":lastName, 
                    "department":department
            }, 200 # As per the user perspective, 200 response represents success
        
        # Handle unexpected errors and return a server error response
        # e is an object of Exception
        except Exception as e:
            return {"success": False,"errors": [str(e)]}, 500
        
    def get_doctor_details(self, doctor_id):
        try:
            if not doctor_id or not doctor_id.strip():
                return {"success": False, "errors": ["Doctor ID is required"]}, 400

            # Validate if the doctor_id is a valid UUID
            if not self._valid_uuid(doctor_id):
                return{"success":False, "error":["Invalid Doctor ID format"]}, 400

            doctor = self.doctor_repo.get_doctor_by_id(doctor_id)
            if not doctor:
                return {"success": False, "errors": ["Doctor not found"]}, 404

            return {
                "success": True,
                "id": doctor["id"],
                "firstName": doctor["firstName"],
                "lastName": doctor["lastName"],
                "department": doctor["department"]
            }, 200 # As per the user perspective, 200 response represents success
        
        # Handle unexpected errors and return a server error response
        # e is an object of Exception
        except Exception as e:
            return {"success": False, "errors": [str(e)]}, 500
        
    #Searches for doctors whose first name or last name or department matches the provided name.
    def search_doctors_by_name(self, name):
        try:
            # Check if name parameter is missing or empty.
            if not name or not name.strip():
                return {"success": False, 
                        "errors": ["Name is required"]
                }, 400
            # Call repository method to search doctors by name.
            doctors = self.doctor_repo.search_doctors(name.strip())
    
            if not doctors:
                return {"success": False, 
                        "errors": ["No doctors found matching the name"]
                }, 404
    
            return {"success": True, 
                    "doctors": doctors
            }, 200
        # Handle any unexpected errors and return a server error.
        except Exception as e:
            return {"success": False, 
                    "errors": [str(e)]
            }, 500
  
    def assign_doctor_to_patient(self, data):
        try:
            # Extracting data from the input dictionary
            doctorId = data.get('doctorId')
            patientId = data.get('patientId')
            dateOfAdmission = data.get('dateOfAdmission')
    
            errors = []
            # Validate doctorId
            if not doctorId:
                errors.append("Doctor ID is required")
            elif not self._valid_uuid(doctorId):
                errors.append("Invalid Doctor ID format")

            # Validate patientId
            if not patientId:
                errors.append("Patient ID is required")
            elif not self._valid_uuid(patientId):
                errors.append("Invalid Patient ID format")

            # Validate dateOfAdmission 
            if not dateOfAdmission:
                errors.append("Date of Admission is required")
            else:
                try:
                    # Check if dateOfAdmission is in the correct format
                    datetime.strptime(dateOfAdmission, '%Y-%m-%d')
                except ValueError:
                    errors.append("Date of Admission must be in YYYY-MM-DD format")
    
            if errors:
                return {"success": False, "errors": errors}, 400
    
            result = self.doctor_repo.assign_doctor_to_patient(doctorId, patientId, dateOfAdmission)
    
            if not result:
                return {"success": False, "errors": ["Failed to assign doctor to patient"]}, 400
    
            return {"success": True}, 200
        
        # Handle unexpected errors and return a server error response
        # e is an object of Exception
        except Exception as e:
            return {"success": False, "errors": [str(e)]}, 500
        
    def get_assigned_doctors_by_patient(self, patient_id):
        try:
            # Validations.
            if not patient_id or not patient_id.strip():
                return {"success": False, "errors": ["Patient ID is required"]}, 400
    
            if not self._valid_uuid(patient_id):
                return {"success": False, "errors": ["Invalid Patient ID format"]}, 400
    
            # Call repository to get the doctor-patient assignment list.
            doctor_data = self.doctor_repo.get_assigned_doctors_by_patient(patient_id)
    
            if not doctor_data:
                return {"success": False, "errors": ["No doctor assigned to this patient"]}, 404
    
            return {"success": True, "data":doctor_data}, 200
        
        # Handle unexpected errors and return a server error response.
        # e is an object of Exception.
        except Exception as e:
            return {"success": False, "errors": [str(e)]}, 500
        
    def delete_doctor(self, doctor_id):
        try:
            # Validate input
            if not doctor_id or not doctor_id.strip():
                return {"success": False, "errors": ["Doctor ID is required"]}, 400
 
            if not self._valid_uuid(doctor_id):
                return {"success": False, "errors": ["Invalid Doctor ID format"]}, 400
 
            # Delete doctor if not assigned
            result = self.doctor_repo.delete_doctor_if_unassigned(doctor_id)
 
            if result["success"]:
                return {"success": True, "message": "Doctor deleted successfully"}, 200
 
            delete_status = result.get("delete_status")
            if delete_status == "assigned":
                return {"success": False, "errors": ["Doctor is assigned to a patient and cannot be deleted"]}, 400
            elif delete_status == "not_found_or_failed":
                return {"success": False, "errors": ["Failed to delete doctor"]}, 500
            elif delete_status == "exception":
                return {"success": False, "errors": [result.get("error", "Unknown error")]}, 500
            else:
                return {"success": False, "errors": ["Unexpected error occurred"]}, 500
 
        except Exception as e:
            return {"success": False, "errors": [str(e)]}, 500
