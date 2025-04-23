import uuid
from app.database.db_connection import Database

class PatientRepository:
    def __init__(self):
        # Initialize the Database instance to interact with the database
        self.db = Database()
 
    def add_patient(self, firstName, lastName):
        try:
            # Establishing database connection
            connection = self.db.connect()
            # Creating cursor for executing SQL query
            cursor = connection.cursor()
            # Generate a new UUID for the patient ID
            patient_id = str(uuid.uuid4())
 
            # SQL query to insert a new patient
            query = "INSERT INTO patient (id, firstName, lastName) VALUES (%s, %s, %s)"
            cursor.execute(query, (patient_id, firstName, lastName))
            connection.commit()
 
            return patient_id
        
        except Exception as e:
            # Print error message if insertion fails
            print(f"Error inserting patient: {e}")
            return None
        
        finally:
            # Close the cursor and database connection
            if 'cursor' in locals() and cursor:    
                cursor.close()
            self.db.close()

    def get_patient_by_id(self, patient_id):
        try:
            # Establishing database connection
            connection = self.db.connect()
            # Creating cursor for executing SQL query
            cursor = connection.cursor()

            # SQL query to fetch a patient by ID
            query = "SELECT id, firstName, lastName FROM patient WHERE id = %s"
            cursor.execute(query, (patient_id,))
            patient = cursor.fetchone()

            # Check if patient exists
            if patient:
                return {
                    "id": patient[0],
                    "firstName": patient[1],
                    "lastName": patient[2]
                }
            else:
                return None
        
        except Exception as e:
            # Print error message if fetching fails
            print(f"Error fetching patient: {e}")
            return None
        
        finally:
            # Close the cursor and database connection
            if 'cursor' in locals() and cursor:    
                cursor.close()
            self.db.close()

    def get_patient_by_name_combined(self, name, last_name=None):
        try:
            connection = self.db.connect()
            cursor = connection.cursor()
    
            search_value = f"%{name.replace(' ', '').lower()}%"
            if last_name:
                last_name_value = f"%{last_name.replace(' ', '').lower()}%"
            else:
                last_name_value = search_value 
    
            query = """
                SELECT id, firstName, lastName
                FROM patient
                WHERE LOWER(REPLACE(firstName, ' ', '')) LIKE %s
                OR LOWER(REPLACE(lastName, ' ', '')) LIKE %s;
            """
            cursor.execute(query, (search_value, last_name_value))
            results = cursor.fetchall()
    
            if results:
                return [{"id": r[0], "firstName": r[1], "lastName": r[2]} for r in results]
            else:
                return None
        except Exception as e:
            print(f"Error fetching patients by combined name: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def remove_doctor_assignment(self, doctor_id, patient_id):
        try:
            connection = self.db.connect()
            cursor = connection.cursor()
    
            # Check if such an assignment exists and is currently assigned
            check_query = """
                SELECT * FROM doctorpatientassignment
                WHERE doctor_id = %s AND patient_id = %s AND is_unassigned = FALSE
            """
            cursor.execute(check_query, (doctor_id, patient_id))
            if not cursor.fetchone():
                return False  # No match found
    
            # Update the is_unassigned flag to TRUE
            update_query = """
                UPDATE doctorpatientassignment
                SET is_unassigned = TRUE
                WHERE doctor_id = %s AND patient_id = %s AND is_unassigned = FALSE
            """
            cursor.execute(update_query, (doctor_id, patient_id))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error unassigning doctor: {e}")
            return False
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()
                
    def update_patient(self, patient_id, data):
        connection = self.db.connect()
        cursor = connection.cursor()
        try:
            # Check if the patient is assigned to a doctor
            check_query = "SELECT doctor_id FROM doctorpatientassignment WHERE patient_id = %s"
            cursor.execute(check_query, (patient_id,))
            result = cursor.fetchone()

            if result:
                raise ValueError("Patient is assigned to a doctor and cannot be updated.")

            # Dynamically build the update query based on the provided data
            update_fields = []
            update_values = []

            if 'firstName' in data:
                update_fields.append("first_name = %s")
                update_values.append(data['firstName'].strip())
            if 'lastName' in data:
                update_fields.append("last_name = %s")
                update_values.append(data['lastName'].strip())

            if not update_fields:
                raise ValueError("No valid fields to update")

            update_fields_str = ", ".join(update_fields)
            update_values.append(patient_id)

            query = f"UPDATE patient SET {update_fields_str} WHERE id = %s"
            cursor.execute(query, tuple(update_values))
            connection.commit()

            return True
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def delete_patient(self, patient_id):
        connection = self.db.connect()
        cursor = connection.cursor()
        try:
            # Check if the patient is assigned to a doctor
            check_query = """
            SELECT * FROM doctorpatientassignment
            WHERE patient_id = %s AND is_unassigned = FALSE
            """
            cursor.execute(check_query, (patient_id,))
            assignment = cursor.fetchone()

            if assignment:
                raise ValueError("Patient is assigned to a doctor and cannot be deleted.")

            # If not assigned, delete the patient
            delete_query = "DELETE FROM patient WHERE id = %s"
            cursor.execute(delete_query, (patient_id,))
            connection.commit()

            return True
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
