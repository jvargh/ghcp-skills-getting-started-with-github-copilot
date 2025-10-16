"""
Test configuration and fixtures for the Mergington High School Activities API
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI application"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store original activities
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball training and inter-school matches",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Learn soccer skills and participate in friendly matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["carlos@mergington.edu", "maya@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore various art mediums including painting, drawing, and sculpture",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["zoe@mergington.edu", "lucas@mergington.edu"]
        },
        "Drama Society": {
            "description": "Acting workshops and theatrical performances",
            "schedule": "Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["isabella@mergington.edu", "ethan@mergington.edu"]
        },
        "Debate Club": {
            "description": "Develop public speaking skills and participate in debate competitions",
            "schedule": "Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 14,
            "participants": ["ava@mergington.edu", "noah@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Compete in various science and engineering challenges",
            "schedule": "Saturdays, 9:00 AM - 11:00 AM",
            "max_participants": 18,
            "participants": ["mia@mergington.edu", "liam@mergington.edu"]
        }
    }
    
    # Reset activities to original state
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Clean up after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def sample_activity():
    """Sample activity data for testing"""
    return {
        "description": "Test activity for unit testing",
        "schedule": "Test day, 1:00 PM - 2:00 PM",
        "max_participants": 5,
        "participants": ["test1@mergington.edu", "test2@mergington.edu"]
    }