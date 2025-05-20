import unittest
import json
from unittest.mock import patch
from main import app
 
# Constants
PATIENT_ID = "fcfd3827-a3e5-4c86-bbb5-ab660fea0eb3"
FIRSTNAME = "John"
LASTNAME = "Doe"
DUMMY_ID_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjY2MGVmM2I5Nzg0YmRmNTZlYmU4NTlmNTc3ZjdmYjJlOGMxY2VmZmIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI5NDQ2NjM5MDQ5NzQtZDZzbDI3YWdsMnZ2MWVsanQ5MnR2YjA3bmRkZDN2MHYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI5NDQ2NjM5MDQ5NzQtZDZzbDI3YWdsMnZ2MWVsanQ5MnR2YjA3bmRkZDN2MHYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTU4Njc2NDQzNzA5NTU3MTgwOTciLCJlbWFpbCI6InRvbWNydXNlNTAyMUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6IkNvUTdDcVFLSWhUaGdqNEUxSldxY3ciLCJuYW1lIjoidG9tIGNydXNlIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0tncmhJNGVFQ3lNSXVsUUV1QWhHdUhybnExRkxBNjRrbkhXRWlTQ3VrdF9IZWwydz1zOTYtYyIsImdpdmVuX25hbWUiOiJ0b20iLCJmYW1pbHlfbmFtZSI6ImNydXNlIiwiaWF0IjoxNzQ3NzEzNjU0LCJleHAiOjE3NDc3MTcyNTR9.LlPEkpAu1v5rpy1Wpm-6Ro6gNrs97rllMQyXH_yw-3qnFrJB4-8a05haqBrwLaagozGSNH5lS1LhH84MAo0YUAkexwraVMjeUeSiv-b1OqI5zXbIVhA907R-kFGoqLYOYRtmbt9dG39zHwXrt9CVm1QxcBxcaW33kEX2HF9HRZJjoDPlokmtUE2E9QypIum404xvtbJiMZmOKPVk9_hoc3dlLNZHvBmIVpGwxGZ-SnT8A8-c9HA3cf929SCufck2H3e_FDazdMolXmdSCczGveG_f40uuc_Osoq06lctW4OpAPEEp5KWSDKV_rKxklGCPcQEE0-3WgpuTzvjjDyKhw"
 
class TestGetPatientByIdAPI(unittest.TestCase):  
    # Inherits from unittest.TestCase for test features
    def setUp(self):
        self.client = app.test_client()
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {DUMMY_ID_TOKEN}'
        }
 
    # Test Case 1: Successfully fetching a patient by ID
    @patch('app.services.patient_services.PatientService.get_patient_by_id')
    def test_get_patient_success(self, mock_get):
        # Arrange: mock only the dictionary, no status code tuple
        mock_get.return_value = {
            "success": True,
            "id": PATIENT_ID,
            "firstName": FIRSTNAME,
            "lastName": LASTNAME
        }
    
        # Act
        response = self.client.get(f"/patient/{PATIENT_ID}", headers=self.headers)
    
        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["id"], PATIENT_ID)
        self.assertEqual(data["firstName"], FIRSTNAME)
        self.assertEqual(data["lastName"], LASTNAME)

    # Test Case 2: Fetching a patient with invalid ID format
    def test_get_patient_invalid_id_format(self):
        # Act: Pass a wrong ID format (like a string instead of UUID)
        response = self.client.get("/patient/fcfd3827-a3e5-4c86-bbb5-ab660f", headers=self.headers)

        # Assert: Should return 400 Bad Request
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        print(data)
        self.assertIn("Invalid Patient ID format", data["errors"])

    # Test Case 3: Fetching a patient that does not exist
    def test_get_patient_nonexistent(self):
        # Act: Try to fetch a patient with a valid format but non-existing ID
        response = self.client.get(f"/patient/fcfd3827-a3e5-4c86-bbb5-ab660fea0ec4", headers=self.headers)

        # Assert: Should return 404 Not Found
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("Patient not found", data["errors"])

    #Test Case 4: Giving an empty id in the url
    def test_get_patient_no_id(self):
        response = self.client.get(f"/patient/ ", headers=self.headers)

        # Assert: Should return 400 Bad Request
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("Patient ID is required", data["errors"])

    # Test Case 5: Giving an invalid URL path
    def test_get_patient_invalid_path(self):
        response = self.client.get(f"/pat", headers=self.headers)

        # Assert: Should return 404 Not Found
        self.assertEqual(response.status_code, 404)

# Run the tests
if __name__ == '__main__':
    unittest.main()
