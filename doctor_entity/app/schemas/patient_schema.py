from marshmallow import Schema, fields, validates, ValidationError
 
class PatientSchema(Schema):
    patient_id = fields.Int(dump_only=True)  
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    
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
