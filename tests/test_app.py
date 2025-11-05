import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    """Test that the root endpoint redirects to static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities

def test_signup_success():
    """Test successful activity signup"""
    activity_name = "Chess Club"
    email = "test@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

def test_signup_already_registered():
    """Test signup when student is already registered"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # This email is already registered in the test data
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_activity_not_found():
    """Test signup for non-existent activity"""
    activity_name = "Non Existent Club"
    email = "test@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_success():
    """Test successful activity unregistration"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # This email is in the test data
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

def test_unregister_not_registered():
    """Test unregistration when student is not registered"""
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]

def test_unregister_activity_not_found():
    """Test unregistration from non-existent activity"""
    activity_name = "Non Existent Club"
    email = "test@mergington.edu"
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]