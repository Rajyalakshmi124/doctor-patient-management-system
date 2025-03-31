from app.utils.db import Database

class PatientRepository:
    def __init__(self):
        self.db = Database()
 
    def add_patient(self, first_name, last_name):
        
        try:
            connection = self.db.connect()
            cursor = connection.cursor()
 
            query = "INSERT INTO patient (first_name, last_name) VALUES (%s, %s)"
            cursor.execute(query, (first_name, last_name))
            connection.commit()
 
            patient_id = cursor.lastrowid  
            return patient_id
        
        except Exception as e:
            print(f"Error inserting patient: {e}")
            return None
        
        finally:
            if 'cursor' in locals() and cursor:    
                cursor.close()
            self.db.close()
