from app.database.db_connection import Database
import uuid

class DoctorRepository:
    # Initializes the DoctorRepository class and sets up a database connection instance.
    def __init__(self):
        self.db = Database()

    def add_doctor(self, firstName, lastName, department):
        try:
            # Establishing database connection
            connection = self.db.connect()
            # Creating cursor to execute SQL queries
            cursor = connection.cursor()
            doctor_id = str(uuid.uuid4())
            # SQL query to insert a new Doctor
            query = "INSERT INTO doctor(id, firstName, lastName, department) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (doctor_id, firstName, lastName, department))
            connection.commit()
            return doctor_id
        
        except Exception as e:
            print(f"Error inserting doctor: {e}")
            return None
        
        finally:
            cursor.close()
            connection.close()

    def get_doctor_by_id(self, doctor_id):
        try:
            connection = self.db.connect()
            # Creating cursor to execute SQL queries
            cursor = connection.cursor()
            query = "SELECT id, firstName, lastName, department FROM doctor WHERE id = %s"
            cursor.execute(query, (doctor_id,))
            doctor = cursor.fetchone()
            # check if doctor exists
            if doctor:
                return {
                    "id": doctor[0],
                    "firstName": doctor[1],
                    "lastName": doctor[2],
                    "department": doctor[3]
                }
            return None
            
        # e is an object of Exception
        except Exception as e:
            print(f"Error fetching doctor: {e}")
            return None
        
        finally:
            cursor.close()
            connection.close()

    #Searches for doctors by first name or last name or department matching the given name using SQL LIKE.
    def search_doctors(self, name):
        try:
            connection = self.db.connect()
            cursor = connection.cursor()

            # SQL query to search doctors by first name, last name, full name, or department
            query = """
            SELECT id, firstName, lastName, department 
            FROM doctor 
            WHERE firstName LIKE %s 
            OR lastName LIKE %s 
            OR CONCAT(firstName, ' ', lastName) LIKE %s 
            OR department LIKE %s
            """
            like_pattern = f"%{name}%"
            cursor.execute(query, (like_pattern, like_pattern, like_pattern, like_pattern))
            # Fetch all matching records.
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
        finally:
            cursor.close()
            connection.close()

    # Assigns a doctor to a patient in the database.
    def assign_doctor_to_patient(self, doctorId, patientId, dateOfAdmission):
        try:
            connection = self.db.connect()
            cursor = connection.cursor()
            # Generate a UUID for doctor-patient assignment
            assign_id= str(uuid.uuid4())
            query = """
                INSERT INTO doctorpatientassignment (id,doctorId, patientId, dateOfAdmission)
                VALUES (%s, %s, %s, %s)
            """
            # Execute the insert query with provided values.
            cursor.execute(query, (assign_id, doctorId, patientId, dateOfAdmission))
            connection.commit()
            return True
 
        except Exception as e:
            print(f"Error assigning doctor to patient: {e}")
            return False
 
        finally:
            cursor.close()
            connection.close()
 
    def get_assigned_doctors_by_patient(self, patient_id):
        try:
            connection = self.db.connect()
            cursor = connection.cursor()

            # SQL query to get all doctors assigned to the given patient
            query = """
                SELECT d.id, d.firstName, d.lastName, d.department, dp.dateOfAdmission
                FROM doctorpatientassignment dp
                JOIN doctor d ON dp.doctorId = d.id
                WHERE dp.patientId = %s
            """
            # Execute the query with patient_id as parameter
            cursor.execute(query, (patient_id,))
            rows = cursor.fetchall()

            if not rows:
                return None

            # Prepare the response list of doctors.
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
            return {
                "doctors": doctors
            }

        except Exception as e:
            print(f"Error fetching assigned doctors: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

    def update_doctor(self, doctor_id, firstName, lastName, department):
        try:
            connection = self.db.connect()
            cursor = connection.cursor()

            # Build the update query dynamically based on provided fields
            update_fields = []
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
            connection.commit()

            return cursor.rowcount > 0

        except Exception as e:
            print(f"Error updating doctor: {e}")
            return False

        finally:
            cursor.close()
            connection.close()
       