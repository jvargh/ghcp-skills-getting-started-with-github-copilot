"""
Tests for the basic API endpoints and functionality
"""
import pytest
from fastapi import status
from src.app import activities


class TestBasicEndpoints:
    """Test basic API endpoints"""
    
    def test_root_redirect(self, client):
        """Test that root endpoint redirects to static index"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        # Should redirect to static files
        assert "index.html" in str(response.url) or response.is_redirect
    
    def test_get_activities(self, client, reset_activities):
        """Test GET /activities endpoint"""
        response = client.get("/activities")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        
        # Check structure of activities
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)
    
    def test_activities_contain_expected_data(self, client, reset_activities):
        """Test that activities contain expected initial data"""
        response = client.get("/activities")
        data = response.json()
        
        # Check for some expected activities
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        
        # Check Chess Club specifically
        chess_club = data["Chess Club"]
        assert chess_club["max_participants"] == 12
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]