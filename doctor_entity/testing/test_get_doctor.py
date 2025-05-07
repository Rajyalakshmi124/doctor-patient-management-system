import pytest
from testing.test_doctor_api import FIRSTNAME, LASTNAME, DEPARTMENT, UUID
from unittest.mock import patch
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
 
# Test case for successful doctor retrieval
def test_get_doctor_success(client):
    mock_response = {
        "success": True,
        "id": UUID,
        "firstName": FIRSTNAME,
        "lastName": LASTNAME,
        "department": DEPARTMENT
    }
 
    with patch("app.services.doctor_service.DoctorService.get_doctor_details", return_value=(mock_response, 200)):
        response = client.get("/doctor/d3a85b22-26b7-40e8-938c-b237eb298cdb")
        assert response.status_code == 200
        assert response.get_json() == mock_response
    
#Test case for doctor ID is required
def test_get_doctor_required(client):
    mock_response = {
        "success": False,
        "errors": ["Doctor ID is required"]
    }
    
    with patch("app.services.doctor_service.DoctorService.get_doctor_details", return_value=(mock_response, 400)):
        response = client.get("/doctor/ ")
        assert response.status_code == 400
        assert response.get_json() == mock_response
 
# Test case for doctor not found
def test_get_doctor_not_found(client):
    mock_response = {
        "success": False,
        "errors": ["Doctor not found"]
    }
 
    with patch("app.services.doctor_service.DoctorService.get_doctor_details", return_value=(mock_response, 404)):
        response = client.get("/doctor/d3a85b22-26b7-40e8-938c-b237eb298cdc")
        assert response.status_code == 404
        assert response.get_json() == mock_response
 
# Test case for invalid doctor ID format
def test_get_doctor_invalid_id(client):
    mock_response = {
        "success": False,
        "errors": ["Invalid Doctor ID format"]
    }
 
    with patch("app.services.doctor_service.DoctorService.get_doctor_details", return_value=(mock_response, 400)):
        response = client.get("/doctor/d3a85b22-26b7-40e8-938c")
        assert response.status_code == 400
        assert response.get_json() == mock_response
 
def test_get_doctor_route_negative(client):
    response = client.get("/doc")
    assert response.status_code == 404, "Expected status code 404"
