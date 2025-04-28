import unittest
import json
from main import app

class TestGetPatientByIdAPI(unittest.TestCase):
    # Inherits from unittest.TestCase to access built-in testing features

    def setUp(self):
        # Set up test client to simulate API requests
        self.client = app.test_client()
        self.headers = {'Content-Type': 'application/json'}

    # Test Case 1: Successfully fetching a patient by ID
    def test_get_patient_success(self):
        # Act: Fetch the patient using GET with a known valid ID
        patient_id = "fcfd3827-a3e5-4c86-bbb5-ab660fea0eb2"  
        get_response = self.client.get(f"/patient/{patient_id}", headers=self.headers)

        # Assert: Check the fetched data is correct
        self.assertEqual(get_response.status_code, 200)
        get_data = json.loads(get_response.data)
        self.assertTrue(get_data["success"])
        self.assertEqual(get_data["firstName"], "John")
        self.assertEqual(get_data["lastName"], "Doe")
        self.assertEqual(get_data["id"], patient_id)

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

# Run the tests
if __name__ == '__main__':
    unittest.main()
