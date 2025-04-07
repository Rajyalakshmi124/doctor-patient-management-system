from app.database.db_connection import Database
 
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
            query = "INSERT INTO doctor(firstName, lastName, department) VALUES (%s, %s, %s)"
            cursor.execute(query, (firstName, lastName, department))
            connection.commit()
 
            doctor_id = cursor.lastrowid
            return doctor_id
       
        # Handling any errors that occur during thedatabase operation
        # e is an object of Exception
        except Exception as e:
            print(f"Error inserting doctor: {e}")
            return None
        
        # Ensuring that resources are properly closed after execution
        finally:
            cursor.close()
            self.db.close()

    def get_doctor_by_id(self, doctor_id):
        """
        Fetches a doctor's details from the database using their ID.
        """
        try:
            connection = self.db.connect()
            # Create a cursor object to execute SQL queries.
            cursor = connection.cursor()
            query = "SELECT id, firstName, lastName, department FROM doctor WHERE id = %s"
            cursor.execute(query, (doctor_id))
            doctor = cursor.fetchone()
            if doctor:
                return{
                    "id": doctor[0],
                    "firstName": doctor[1],
                    "lastName": doctor[2],
                    "department": doctor[3]
                }
            else:
                return None
        # Handling any errors that occur during thedatabase operation
        # e is an object of Exception
        except Exception as e:
            print(f"Error fetching doctor: {e}")
            return None
        
        finally:
            cursor.close()
            self.db.close()
