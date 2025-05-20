import unittest
import json
from unittest.mock import patch
from main import app
 
PATIENT_ID = "11111111-1111-1111-1111-111111111111"  # Use a valid UUID for testing
DUMMY_ID_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjY2MGVmM2I5Nzg0YmRmNTZlYmU4NTlmNTc3ZjdmYjJlOGMxY2VmZmIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI5NDQ2NjM5MDQ5NzQtZDZzbDI3YWdsMnZ2MWVsanQ5MnR2YjA3bmRkZDN2MHYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI5NDQ2NjM5MDQ5NzQtZDZzbDI3YWdsMnZ2MWVsanQ5MnR2YjA3bmRkZDN2MHYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTU4Njc2NDQzNzA5NTU3MTgwOTciLCJlbWFpbCI6InRvbWNydXNlNTAyMUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6IkNvUTdDcVFLSWhUaGdqNEUxSldxY3ciLCJuYW1lIjoidG9tIGNydXNlIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0tncmhJNGVFQ3lNSXVsUUV1QWhHdUhybnExRkxBNjRrbkhXRWlTQ3VrdF9IZWwydz1zOTYtYyIsImdpdmVuX25hbWUiOiJ0b20iLCJmYW1pbHlfbmFtZSI6ImNydXNlIiwiaWF0IjoxNzQ3NzEzNjU0LCJleHAiOjE3NDc3MTcyNTR9.LlPEkpAu1v5rpy1Wpm-6Ro6gNrs97rllMQyXH_yw-3qnFrJB4-8a05haqBrwLaagozGSNH5lS1LhH84MAo0YUAkexwraVMjeUeSiv-b1OqI5zXbIVhA907R-kFGoqLYOYRtmbt9dG39zHwXrt9CVm1QxcBxcaW33kEX2HF9HRZJjoDPlokmtUE2E9QypIum404xvtbJiMZmOKPVk9_hoc3dlLNZHvBmIVpGwxGZ-SnT8A8-c9HA3cf929SCufck2H3e_FDazdMolXmdSCczGveG_f40uuc_Osoq06lctW4OpAPEEp5KWSDKV_rKxklGCPcQEE0-3WgpuTzvjjDyKhw"

class TestPatchPatientAPI(unittest.TestCase):
    # Inherits from unittest.TestCase for test features
    def setUp(self):
        self.client = app.test_client()
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {DUMMY_ID_TOKEN}'
        }

    # Test Case 1: Successfully updating a patient
    @patch('app.services.patient_services.PatientService.update_patient_by_id')
    def test_update_patient_success(self, mock_update):
        mock_update.return_value = ({
            "success": True,
            "message": "Patient details updated successfully."
        }, 200)
 
        payload = {
            "firstName": "Jane",
            "lastName": "Smith"
        }
 
        response = self.client.patch(f"/patient/{PATIENT_ID}", data=json.dumps(payload), headers=self.headers)
 
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("message", data)
 
    # Test Case 2: Invalid patient ID format
    def test_patch_patient_invalid_id_format(self):
        # Arrange: Invalid ID
        invalid_id = "fcfd3827-a3e5-4c86-bbb5-ab660fe"
        payload = {
            "firstName": "UpdatedFirstName",
            "lastName": "UpdatedLastName"
        }
        # Act: Send PATCH request
        response = self.client.patch(f"/patient/{invalid_id}", data=json.dumps(payload), headers=self.headers)
 
        # Assert: Should return 400 Bad Request
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("Invalid Patient ID format", data["errors"])
 
    # Test Case 3: Patient not found
    def test_patch_patient_nonexistent(self):
        # Arrange: Non-existing ID
        non_existing_id = "fcfd3827-a3e5-4c86-bbb5-ab660fea0ec4"
        payload = {
            "firstName": "UpdatedFirstName",
            "lastName": "UpdatedLastName"
        }
        # Act: Send PATCH request
        response = self.client.patch(f"/patient/{non_existing_id}", data=json.dumps(payload), headers=self.headers)
 
        # Assert: Should return 404 Not Found
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("Patient not found", data["errors"])
 
    # Test Case 4: Missing payload (no data provided)
    def test_patch_patient_no_payload(self):
        # Arrange: Valid patient ID, but no body
        patient_id = "fcfd3827-a3e5-4c86-bbb5-ab660fea0eb2"
        # Act: Send PATCH request with empty data
        response = self.client.patch(f"/patient/{patient_id}", data=json.dumps({}), headers=self.headers)
 
        # Assert: Should return 400 Bad Request
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("Request body must be JSON.", data["errors"])
 
    # Test Case 5: Empty ID in URL
    def test_patch_patient_no_id(self):
        # Act: Send PATCH request with no ID
        response = self.client.patch(f"/patient/ ", data=json.dumps({"firstName": "Test"}), headers=self.headers)
 
        # Assert: Should return 400 Bad Request
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("Patient ID is required", data["errors"])
 
# Run the tests
if __name__ == '__main__':
    unittest.main()
