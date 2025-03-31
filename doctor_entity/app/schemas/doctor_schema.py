from marshmallow import Schema, fields, validates, ValidationError
 
class DoctorSchema(Schema):
    # Defines the schema for doctor data validation using marshmallow
    doctor_id = fields.Int(dump_only=True)  
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    dept_name = fields.Str(required=True)
   
    # Ensures first_name is alphabetic and not empty.
    @validates("first_name")
    def validate_first_name(self, value):
        if not value.isalpha():
            raise ValidationError("First name must contain only letters.")
   
    # Ensures last_name is alphabetic and not empty.
    @validates("last_name")
    def validate_last_name(self, value):
        if not value.isalpha():
            raise ValidationError("Last name must contain only letters.")
    
    # Ensures dept_name is alphabetic, not empty, and a valid string
    @validates("dept_name")
    def validate_dept_name(self, value):
        if not isinstance(value, str) or not value.strip().isalpha():
            raise ValidationError("dept name must contain only letters.")
