class Patient:
    def __init__(self, patient_id=None, first_name="", last_name=""):
        self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
    
    # Converts Patient object to a dictionary.
    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "first_name": self.first_name,
            "last_name": self.last_name
        }
