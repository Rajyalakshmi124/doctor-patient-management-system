from doctor_entity.app.db_connection.db_connection import Database
 
class DoctorRepository:
    def __init__(self):
        """
        Initializes the DoctorRepository class and sets up a database connection instance.
        """
        self.db = Database()
 
    def add_doctor(self, first_name, last_name, dept_name):
       
        try:
            # Establishing database connection
            connection = self.db.connect()
            # Creating cursor to execute SQL queries
            cursor = connection.cursor()
            query = "INSERT INTO doctor(first_name, last_name, dept_name) VALUES (%s, %s, %s)"
            cursor.execute(query, (first_name, last_name, dept_name))
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
