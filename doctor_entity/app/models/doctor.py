class Doctor:
    """
    A class representing a Doctor entity
    """
    def __init__(self, doctor_id=None, first_name="", last_name="", dept_name=""):
        self.doctor_id = doctor_id
        self.first_name = first_name
        self.last_name = last_name
        self.dept_name = dept_name
   
    # Converts Doctor object to a dictionary.
    def to_dict(self):
        return {
            "doctor_id": self.doctor_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dept_name": self.dept_name
        }
