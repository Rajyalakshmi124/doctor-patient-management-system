from app.db_connection.db_connection import Database

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
 
            # SQL query to insert a new patient
            query = "INSERT INTO patient (first_name, last_name) VALUES (%s, %s)"
            cursor.execute(query, (firstName, lastName))
            connection.commit()
 
            # Get the ID of the newly inserted patient
            patient_id = cursor.lastrowid  
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