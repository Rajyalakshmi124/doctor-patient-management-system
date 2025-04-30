import unittest
import json
from unittest.mock import patch
from main import app
 
# Constants
FIRSTNAME = "Alice"
LASTNAME = "Smith"
 
class TestPostPatientAPI(unittest.TestCase):
    # Inherits from unittest.testTestcase which gives access to built-in testing tools
    def setUp(self):
        # Set up test client for sending HTTP requests
        self.client = app.test_client()
        self.headers = {'Content-Type': 'application/json'}
 
    # Test Case 1: Valid patient creation
    @patch('app.services.patient_services.PatientService.create_patient')  
    def test_post_patient_success(self, mock_create):
        # Arrange: mock return value
        mock_create.return_value = (
                                {
                                    "success": True,
                                    "id": "bf2812ce-6c2f-44fb-aa5e-86425c27db05",
                                    "firstName": FIRSTNAME,
                                    "lastName": LASTNAME
                                },
                                201
                            )
        # Arrange: Prepare valid payload
        payload = {
            "firstName": FIRSTNAME,
            "lastName": LASTNAME
        }

        # Act: Make POST request to /patient
        # json.dumps is used to convert the dict into json format
        response = self.client.post("/patient", data=json.dumps(payload), headers=self.headers)
 
        # Assert: Check for success response
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["firstName"], FIRSTNAME)
        self.assertEqual(data["lastName"], LASTNAME)
        # Use assertIn to check that the specific response is present in the response data 
        self.assertIn("id", data)
 
    # Test Case 2: Missing last name
    def test_post_patient_missing_last_name(self):
        # Missing last name
        payload = { "firstName": FIRSTNAME, "lastName":"" }  
        # Make POST request to /patient
        response = self.client.post("/patient", data=json.dumps(payload), headers=self.headers)
 
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        # Use assertIn to check that the specific error message is present in the response data
        self.assertIn("First name and last name are required", data["errors"])
 
    # Test Case 3: Missing last name
    def test_post_patient_missing_first_name(self):
        # Missing first name
        payload = { "firstName": "", "lastName":LASTNAME }  
        # Make POST request to /patient
        response = self.client.post("/patient", data=json.dumps(payload), headers=self.headers)
 
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("First name and last name are required", data["errors"])
 
    # Test Case 4: Invalid characters in names
    def test_post_patient_invalid_characters(self):
        payload = {
            "firstName": "Ali1s",
            "lastName": "Smi%h"
        }
        # Make POST request to /patient
        response = self.client.post("/patient", data=json.dumps(payload), headers=self.headers)
 
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("First name must contain only letters and spaces", data["errors"])
        self.assertIn("Last name must contain only letters and spaces", data["errors"])
 
    # Test Case 5: Extra fields that are not allowed
    def test_post_patient_with_extra_fields(self):
        payload = {
            "firstName": FIRSTNAME,
            "lastName": LASTNAME,
            "age": 25  # Extra field not allowed
        }
        # Make POST request to /patient
        response = self.client.post("/patient", data=json.dumps(payload), headers=self.headers)
 
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("Only first name and last name are allowed", data["errors"])
   
    # Test Case 6: Non-JSON body
    def test_post_patient_with_non_json_body(self):
        payload = {
 
        }
        # Make POST request to /patient
        response = self.client.post("/patient", data=json.dumps(payload), headers=self.headers)
 
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("Request body must be JSON.", data["errors"])
 
# Run the tests
if __name__ == '__main__':
    unittest.main()
