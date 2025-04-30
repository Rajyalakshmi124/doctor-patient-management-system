import unittest
import json
from unittest.mock import patch
from main import app
 
# Constants
PATIENT_ID = "fcfd3827-a3e5-4c86-bbb5-ab660fea0eb3"
FIRSTNAME = "John"
LASTNAME = "Doe"
 
class TestGetPatientByIdAPI(unittest.TestCase):  
    # Inherits from unittest.TestCase for test features
    def setUp(self):
        # Set up test client to simulate API requests
        self.client = app.test_client()
        self.headers = {'Content-Type': 'application/json'}
 
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
