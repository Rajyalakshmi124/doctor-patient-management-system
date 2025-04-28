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

# Test case for successful doctor creation
def test_post_doctor(client):
    test_data = {
        "firstName": "Robert",
        "lastName": "Miller",
        "department": "Dermatology"
    }

    mock_response = {
        "success": True,
        "id": "d3a85b22-26b7-40e8-938c-b237eb298cda",
        "firstName": "Robert",
        "lastName": "Miller",
        "department": "Dermatology"
    }

    with patch("app.services.doctor_service.DoctorService.create_doctor", return_value=(mock_response, 200)):
        response = client.post("/doctor", json=test_data)
        assert response.status_code == 200
        assert response.get_json() == mock_response

# Test case for validation error: missing first name
def test_post_doctor_validation_error(client):
    test_data = {
        "firstName": "",
        "lastName": "Miller",
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

        response = client.post("/doctor", json=test_data)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["success"] is False
        assert "First name is required" in json_data["errors"]

# Test case for validation error: missing last name
def test_post_doctor_lastname_error(client):
    test_data = {
        "firstName": "Robert",
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

        response = client.post("/doctor", json=test_data)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["success"] is False
        assert "Last name is required" in json_data["errors"]

# Test case for validation error: invalid characters in first name
def test_post_doctor_invalid_firstname(client):
    test_data = {
        "firstName": "Robert123",
        "lastName": "Miller",
        "department": "Dermatology"
    }

    with patch("app.services.doctor_service.DoctorService.create_doctor") as mock_create:
        mock_create.return_value = ({
            "success": False,
            "errors": [
                "First name must contain only letters and spaces"
            ]
        }, 400)

        response = client.post("/doctor", json=test_data)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["success"] is False
        assert "First name must contain only letters and spaces" in json_data["errors"]

# Test case for validation error: invalid characters in last name
def test_post_doctor_invalid_lastname(client):
    test_data = {
        "firstName": "Robert",
        "lastName": "Miller123",
        "department": "Dermatology"
    }

    with patch("app.services.doctor_service.DoctorService.create_doctor") as mock_create:
        mock_create.return_value = ({
            "success": False,
            "errors": [
                "Last name must contain only letters and spaces"
            ]
        }, 400)

        response = client.post("/doctor", json=test_data)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["success"] is False
        assert "Last name must contain only letters and spaces" in json_data["errors"]

# Test case for validation error: invalid characters in department name
def test_post_doctor_invalid_department(client):
    test_data = {
        "firstName": "Robert",
        "lastName": "Miller",
        "department": "123Dermatology"
    }

    with patch("app.services.doctor_service.DoctorService.create_doctor") as mock_create:
        mock_create.return_value = ({
            "success": False,
            "errors": [
                "Department name must contain only alphabets, spaces, and special symbols"
            ]
        }, 400)

        response = client.post("/doctor", json=test_data)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["success"] is False
        assert "Department name must contain only alphabets, spaces, and special symbols" in json_data["errors"]

# Test case for checking if the route is correct
def test_post_doctor_route(client):
    response = client.post("/doctor")
    assert response.status_code != 404, "Route /doctor not found"

def test_post_doctor_route_negative(client):
    response = client.post("/wrong_endpoint")
    assert response.status_code == 404, "Expected status code 404"