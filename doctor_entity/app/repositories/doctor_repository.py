from app.database.db_connection import Database
import uuid

class DoctorRepository:
    def __init__(self):
        """
        Initializes the DoctorRepository class and sets up a database connection instance.
        """
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
            else:
                return None
            
        # e is an object of Exception
        except Exception as e:
            print(f"Error fetching doctor: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
