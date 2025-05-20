import unittest
import json
from unittest.mock import patch
from main import app
 
# Constants
FIRSTNAME = "Alice"
LASTNAME = "Smith"
DUMMY_ID_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjY2MGVmM2I5Nzg0YmRmNTZlYmU4NTlmNTc3ZjdmYjJlOGMxY2VmZmIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI5NDQ2NjM5MDQ5NzQtZDZzbDI3YWdsMnZ2MWVsanQ5MnR2YjA3bmRkZDN2MHYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI5NDQ2NjM5MDQ5NzQtZDZzbDI3YWdsMnZ2MWVsanQ5MnR2YjA3bmRkZDN2MHYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTU4Njc2NDQzNzA5NTU3MTgwOTciLCJlbWFpbCI6InRvbWNydXNlNTAyMUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6IkNvUTdDcVFLSWhUaGdqNEUxSldxY3ciLCJuYW1lIjoidG9tIGNydXNlIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0tncmhJNGVFQ3lNSXVsUUV1QWhHdUhybnExRkxBNjRrbkhXRWlTQ3VrdF9IZWwydz1zOTYtYyIsImdpdmVuX25hbWUiOiJ0b20iLCJmYW1pbHlfbmFtZSI6ImNydXNlIiwiaWF0IjoxNzQ3NzEzNjU0LCJleHAiOjE3NDc3MTcyNTR9.LlPEkpAu1v5rpy1Wpm-6Ro6gNrs97rllMQyXH_yw-3qnFrJB4-8a05haqBrwLaagozGSNH5lS1LhH84MAo0YUAkexwraVMjeUeSiv-b1OqI5zXbIVhA907R-kFGoqLYOYRtmbt9dG39zHwXrt9CVm1QxcBxcaW33kEX2HF9HRZJjoDPlokmtUE2E9QypIum404xvtbJiMZmOKPVk9_hoc3dlLNZHvBmIVpGwxGZ-SnT8A8-c9HA3cf929SCufck2H3e_FDazdMolXmdSCczGveG_f40uuc_Osoq06lctW4OpAPEEp5KWSDKV_rKxklGCPcQEE0-3WgpuTzvjjDyKhw"
 
class TestPostPatientAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {DUMMY_ID_TOKEN}'
        }
 
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
