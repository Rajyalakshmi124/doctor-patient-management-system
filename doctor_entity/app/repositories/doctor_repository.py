from app.database.db_connection import Database
from contextlib import contextmanager
import uuid
# Repository class to handle all doctor-related database operations
class DoctorRepository:
    # Initializes the DoctorRepository class and sets up a database connection instance.
    def __init__(self):
        self.db = Database()
 
    @contextmanager
    def _get_connection_and_cursor(self):
        # Context manager to automatically handle opening and closing DB connection and cursor
        connection = self.db.connect()
        cursor = connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()
            connection.close()
 
    def add_doctor(self, firstName, lastName, department):
        # Method uses the context manager to open and close the connection and cursor
        with self._get_connection_and_cursor() as cursor:
            try:
                # Generate a unique ID for the doctor
                doctor_id = str(uuid.uuid4())
                query = "INSERT INTO doctor(id, firstName, lastName, department) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (doctor_id, firstName, lastName, department))
                # Commit the transaction
                cursor.connection.commit()
                return doctor_id
            except Exception as e:
                print(f"Error inserting doctor: {e}")
                return None
           
    # Retrieve doctor details by doctor ID
    def get_doctor_by_id(self, doctor_id):
        with self._get_connection_and_cursor() as cursor:
            try:
                # Prepare the SQL query to fetch doctor details by ID
                query = "SELECT id, firstName, lastName, department FROM doctor WHERE id = %s"
                # Execute select query
                cursor.execute(query, (doctor_id,))
                # Fetch one matching record
                doctor = cursor.fetchone()
                if doctor:
                    return {
                        "id": doctor[0],
                        "firstName": doctor[1],
                        "lastName": doctor[2],
                        "department": doctor[3]
                    }
                return None
            except Exception as e:
                print(f"Error fetching doctor: {e}")
                return None
           
    #Searches for doctors by first name or last name or department matching the given name using SQL LIKE
    def search_doctors(self, name):
        with self._get_connection_and_cursor() as cursor:
            try:
                # SQL query to search doctors by first name, last name, full name, or department
                query = """
                SELECT id, firstName, lastName, department
                FROM doctor
                WHERE firstName LIKE %s
                OR lastName LIKE %s
                OR CONCAT(firstName, ' ', lastName) LIKE %s
                OR department LIKE %s
                """
                # Pattern for partial matching
                like_pattern = f"%{name}%"
                cursor.execute(query, (like_pattern, like_pattern, like_pattern, like_pattern))
                # Fetch all matching rows
                results = cursor.fetchall()
                doctors = []
                for doctor in results:
                    doctors.append({
                        "id": doctor[0],
                        "firstName": doctor[1],
                        "lastName": doctor[2],
                        "department": doctor[3]
                    })
                return doctors
            except Exception as e:
                print(f"Error searching doctors: {e}")
                return None
 
    # Assigns a doctor to a patient in the database.
    def assign_doctor_to_patient(self, doctorId, patientId, dateOfAdmission):
        with self._get_connection_and_cursor() as cursor:
            try:
                # Generate unique assignment ID
                assign_id = str(uuid.uuid4())
                query = """
                    INSERT INTO doctorpatientassignment (id, doctorId, patientId, dateOfAdmission)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (assign_id, doctorId, patientId, dateOfAdmission))
                # Commit the assignment
                cursor.connection.commit()
                return True
            except Exception as e:
                print(f"Error assigning doctor to patient: {e}")
                return False
           
    # Retrieve all doctors assigned to a particular patient
    def get_assigned_doctors_by_patient(self, patient_id):
        with self._get_connection_and_cursor() as cursor:
            try:
                # Get all assigned doctors for the patient
                query = """
                    SELECT d.id, d.firstName, d.lastName, d.department, dp.dateOfAdmission
                    FROM doctorpatientassignment dp
                    JOIN doctor d ON dp.doctorId = d.id
                    WHERE dp.patientId = %s
                """
                cursor.execute(query, (patient_id,))
                rows = cursor.fetchall()
                if not rows:
                    return None
               
                # Prepare the response
                doctors = []
                for row in rows:
                    doctors.append({
                        "id": row[0],
                        "firstName": row[1],
                        "lastName": row[2],
                        "department": row[3],
                        "dateOfAdmission": row[4].strftime('%Y-%m-%d') if row[4] else None
                    })
                # Return the patient and their assigned doctors
                return {"doctors": doctors}
            except Exception as e:
                print(f"Error fetching assigned doctors: {e}")
                return None
           
    # Delete a doctor only if they are not assigned to any patient      
    def delete_doctor_if_unassigned(self, doctor_id):
        with self._get_connection_and_cursor() as cursor:
            try:
                # Check if the doctor is assigned to any patient
                check_query = "SELECT COUNT(*) FROM doctorpatientassignment WHERE doctorId = %s"
                cursor.execute(check_query, (doctor_id,))
                count = cursor.fetchone()[0]
                if count > 0:
                    # Doctor is assigned, cannot delete
                    return {"success": False, "delete_status": "assigned"}
               
                # Delete the doctor if unassigned
                delete_query = "DELETE FROM doctor WHERE id = %s"
                cursor.execute(delete_query, (doctor_id,))
                cursor.connection.commit()
 
                if cursor.rowcount > 0:
                    # Doctor deleted successfully
                    return {"success": True}
                else:
                    # Doctor not found
                    return {"success": False, "delete_status": "not_found_or_failed"}
            except Exception as e:
                print(f"Error deleting doctor: {e}")
                return {"success": False, "delete_status": "exception", "error": str(e)}
 
    # Update doctor details like first name, last name, or department
    def update_doctor(self, doctor_id, firstName, lastName, department):
        with self._get_connection_and_cursor() as cursor:
            try:
                # Fields to update
                update_fields = []
                # Corresponding values
                update_values = []
 
                if firstName:
                    update_fields.append("firstName = %s")
                    update_values.append(firstName.strip())
                if lastName:
                    update_fields.append("lastName = %s")
                    update_values.append(lastName.strip())
                if department:
                    update_fields.append("department = %s")
                    update_values.append(department.strip())
 
                if not update_fields:
                    return False
 
                update_values.append(doctor_id)
                query = f"UPDATE doctor SET {', '.join(update_fields)} WHERE id = %s"
                cursor.execute(query, tuple(update_values))
                cursor.connection.commit()
                # True if rows updated, otherwise False
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error updating doctor: {e}")
                return False
