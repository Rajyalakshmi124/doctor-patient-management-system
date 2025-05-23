import pytest
from unittest.mock import patch
from main import app
from flask_jwt_extended import create_access_token
 
# Constants
FIRSTNAME = "Robert"
LASTNAME = "Miller"
DEPARTMENT = "Dermatology"
UUID = "d3a85b22-26b7-40e8-938c-b237eb298cda"
 
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
 
@pytest.fixture
def jwt_token():
    # Create a JWT token for testing
    with app.app_context():
        token = create_access_token(identity="test_user")
        yield token
 
# Test case for successful doctor creation
def test_post_doctor(client, jwt_token):
    test_data = {
        "firstName": FIRSTNAME,
        "lastName": LASTNAME,
        "department": DEPARTMENT
    }
 
    mock_response = {
        "success": True,
        "id": UUID,
        "firstName": FIRSTNAME,
        "lastName": LASTNAME,
        "department": DEPARTMENT
    }
 
    with patch("app.services.doctor_service.DoctorService.create_doctor", return_value=(mock_response, 200)):
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = client.post("/doctor", json=test_data, headers=headers)
        assert response.status_code == 200
        assert response.get_json() == mock_response
# Test case for validation error: missing first name
def test_post_doctor_validation_error(client, jwt_token):
    test_data = {
        "firstName": "",
        "lastName": LASTNAME,
        "department": "123Dept"
    }
 
    with patch("app.services.doctor_service.DoctorService.create_doctor") as mock_create:
        mock_create.return_value = ({
            "success": False,
            "errors": [
                "First name is required",
                "Department name must contain only alphabets, spaces, and special symbols"
            ]
        }, 400)
 
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = client.post("/doctor", json=test_data, headers=headers)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["success"] is False
        assert "First name is required" in json_data["errors"]
 
# Test case for validation error: missing last name
def test_post_doctor_lastname_error(client, jwt_token):
    test_data = {
        "firstName": FIRSTNAME,
        "lastName": "",
        "department": "123Dept"
    }
 
    with patch("app.services.doctor_service.DoctorService.create_doctor") as mock_create:
        mock_create.return_value = ({
            "success": False,
            "errors": [
                "Last name is required",
                "Department name must contain only alphabets, spaces, and special symbols"
            ]
        }, 400)
 
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = client.post("/doctor", json=test_data, headers=headers)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["success"] is False
        assert "Last name is required" in json_data["errors"]
 
# Test case for validation error: invalid characters in first name
def test_post_doctor_invalid_firstname(client, jwt_token):
    test_data = {
        "firstName": "Robert123",
        "lastName": LASTNAME,
        "department": DEPARTMENT
    }
 
    with patch("app.services.doctor_service.DoctorService.create_doctor") as mock_create:
        mock_create.return_value = ({
            "success": False,
            "errors": [
                "First name must contain only letters and spaces"
            ]
        }, 400)
 
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = client.post("/doctor", json=test_data, headers=headers)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["success"] is False
        assert "First name must contain only letters and spaces" in json_data["errors"]
 
# Test case for validation error: invalid characters in last name
def test_post_doctor_invalid_lastname(client, jwt_token):
    test_data = {
        "firstName": FIRSTNAME,
        "lastName": "Miller123",
        "department": DEPARTMENT
    }
 
    with patch("app.services.doctor_service.DoctorService.create_doctor") as mock_create:
        mock_create.return_value = ({
            "success": False,
            "errors": [
                "Last name must contain only letters and spaces"
            ]
        }, 400)
 
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = client.post("/doctor", json=test_data, headers=headers)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["success"] is False
        assert "Last name must contain only letters and spaces" in json_data["errors"]
 
# Test case for validation error: invalid characters in department name
def test_post_doctor_invalid_department(client, jwt_token):
    test_data = {
        "firstName": FIRSTNAME,
        "lastName": LASTNAME,
        "department": "123Dermatology"
    }
 
    with patch("app.services.doctor_service.DoctorService.create_doctor") as mock_create:
        mock_create.return_value = ({
            "success": False,
            "errors": [
                "Department name must contain only alphabets, spaces, and special symbols"
            ]
        }, 400)
 
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = client.post("/doctor", json=test_data, headers=headers)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["success"] is False
        assert "Department name must contain only alphabets, spaces, and special symbols" in json_data["errors"]
 
# Test case for validation error: extra fields
def test_post_doctor_extra_field(client, jwt_token):
    test_data = {
        "firstName": FIRSTNAME,
        "lastName": LASTNAME,
        "department": DEPARTMENT,
        "location": "UK"
    }
    with patch("app.services.doctor_service.DoctorService.create_doctor") as mock_create:
        mock_create.return_value = ({
            "success": False,
            "errors": ["Only first name, last name and department are allowed"]
        }, 400)
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = client.post("/doctor", json=test_data, headers=headers)
        assert response.status_code == 400
        json_data = response.get_json()
        assert "Only first name, last name and department are allowed" in json_data["errors"]
 
# Test case for checking if the route is correct
def test_post_doctor_route(client, jwt_token):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.post("/doctor", headers=headers)
    assert response.status_code != 404, "Route /doctor not found"
 
def test_post_doctor_route_negative(client, jwt_token):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.post("/doct", headers=headers)
    assert response.status_code == 404, "Expected status code 404"
