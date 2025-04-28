import sys
import os
import pytest
from unittest.mock import patch
from flask import Flask, jsonify, request
 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
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
        "id": "d3a85b22-26b7-40e8-938c-b237eb298cda",
        "firstName": "John",
        "lastName": "Doe",
        "department": "Cardiology"
    }
 
    with patch("app.services.doctor_service.DoctorService.get_doctor_details", return_value=(mock_response, 200)):
        response = client.get("/doctor/d3a85b22-26b7-40e8-938c-b237eb298cda")
        assert response.status_code == 200
        assert response.get_json() == mock_response
 
# Test case for doctor not found
def test_get_doctor_not_found(client):
    mock_response = {
        "success": False,
        "errors": ["Doctor not found"]
    }
 
    with patch("app.services.doctor_service.DoctorService.get_doctor_details", return_value=(mock_response, 404)):
        response = client.get("/doctor/nonexistent-id")
        assert response.status_code == 404
        assert response.get_json() == mock_response
 
# Test case for invalid doctor ID format
def test_get_doctor_invalid_id(client):
    mock_response = {
        "success": False,
        "errors": ["Invalid Doctor ID format"]
    }
 
    with patch("app.services.doctor_service.DoctorService.get_doctor_details", return_value=(mock_response, 400)):
        response = client.get("/doctor/invalid-id")
        assert response.status_code == 400
        assert response.get_json() == mock_response

# Test case for checking if the route is correct
def test_get_doctor_route(client):
    response = client.get("/doctor/d3a85b22-26b7-40e8-938c-b237eb298cda")
    assert response.status_code != 404, "Route /doctor/ not found"
 
def test_get_doctor_route_negative(client):
    response = client.get("/wrong_endpoint")
    assert response.status_code == 404, "Expected status code 404"
