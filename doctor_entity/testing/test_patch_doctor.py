import pytest
from unittest.mock import patch
from main import app
from testing.test_doctor_api import FIRSTNAME, LASTNAME, DEPARTMENT

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
 
# Test case for successful doctor update
def test_patch_doctor_success(client):
    test_data = {
        "firstName": FIRSTNAME,
        "lastName": LASTNAME,
        "department": DEPARTMENT
    }
 
    mock_response = {
        "success": True,
        "message": "Doctor updated successfully"
    }
 
    with patch("app.services.doctor_service.DoctorService.update_doctor", return_value=(mock_response, 200)):
        response = client.patch("/doctor/d3a85b22-26b7-40e8-938c-b237eb298cda", json=test_data)
        assert response.status_code == 200
        assert response.get_json() == mock_response
  
# Test case for invalid doctor ID format
def test_patch_doctor_invalid_id(client):
    test_data = {
        "firstName": FIRSTNAME,
        "lastName": LASTNAME,
        "department": DEPARTMENT
    }

    with patch("app.services.doctor_service.DoctorService.update_doctor") as mock_create:
        mock_create.return_value = ({
            "success": False,
            "errors": ["Invalid doctor ID format"]
        }, 400)
        response = client.patch("/doctor/d3a85b22-26b7-40e8-", json=test_data)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["success"] is False
        assert "Invalid doctor ID format" in json_data["errors"]

 # Test case for validation error: invalid characters in first name
def test_patch_doctor_invalid_firstname(client):
    test_data = {
        "firstName": "Robert123",
        "lastName": LASTNAME,
        "department": DEPARTMENT
    }
   
    with patch("app.services.doctor_service.DoctorService.update_doctor") as mock_create:
        mock_create.return_value = ({
            "success": False,
            "errors": ["First name must contain only letters and spaces"]
        }, 400)
        response = client.patch("/doctor/d3a85b22-26b7-40e8-938c-b237eb298cda", json=test_data)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["success"] is False
        assert "First name must contain only letters and spaces" in json_data["errors"]
 
# Test case for validation error: invalid characters in last name
def test_patch_doctor_invalid_lastname(client):
    test_data = {
        "firstName": FIRSTNAME,
        "lastName": "Miller123",
        "department": DEPARTMENT
    }

    with patch("app.services.doctor_service.DoctorService.update_doctor") as mock_create:
        mock_create.return_value = ({
            "success": False,
            "errors": ["Last name must contain only letters and spaces"]
        }, 400)
        response = client.patch("/doctor/d3a85b22-26b7-40e8-938c-b237eb298cda", json=test_data)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["success"] is False
        assert "Last name must contain only letters and spaces" in json_data["errors"]
 
# Test case for validation error: invalid characters in department name
def test_patch_doctor_invalid_department(client):
    test_data = {
        "firstName": FIRSTNAME,
        "lastName": LASTNAME,
        "department": "123Dermatology"
    }
 
    with patch("app.services.doctor_service.DoctorService.update_doctor") as mock_create:
        mock_create.return_value = ({
            "success": False,
            "errors": ["Department name must contain only alphabets, spaces, and special symbols"]
        }, 400)
        response = client.patch("/doctor/d3a85b22-26b7-40e8-938c-b237eb298cda", json=test_data)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["success"] is False
        assert "Department name must contain only alphabets, spaces, and special symbols" in json_data["errors"]
 
# Test case for checking Invalid route
def test_patch_doctor_route_negative(client):
    response = client.patch("/doct")
    assert response.status_code == 404, "Expected status code 404"
