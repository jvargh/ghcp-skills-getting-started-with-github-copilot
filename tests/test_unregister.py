"""
Tests for unregister functionality
"""
import pytest
from fastapi import status
from src.app import activities


class TestUnregisterFunctionality:
    """Test activity unregister functionality"""
    
    def test_unregister_success(self, client, reset_activities):
        """Test successful unregistration from an activity"""
        # First verify the participant is registered
        assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
        
        response = client.delete(
            "/activities/Chess Club/unregister?email=michael@mergington.edu"
        )
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "message" in data
        assert "michael@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]
        
        # Verify the participant was removed
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    
    def test_unregister_participant_not_registered(self, client, reset_activities):
        """Test unregister participant who is not registered"""
        response = client.delete(
            "/activities/Chess Club/unregister?email=notregistered@mergington.edu"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()
    
    def test_unregister_nonexistent_activity(self, client, reset_activities):
        """Test unregister from non-existent activity"""
        response = client.delete(
            "/activities/Nonexistent Activity/unregister?email=test@mergington.edu"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_unregister_with_url_encoded_activity_name(self, client, reset_activities):
        """Test unregister with URL-encoded activity name"""
        # First verify the participant is registered
        assert "emma@mergington.edu" in activities["Programming Class"]["participants"]
        
        response = client.delete(
            "/activities/Programming%20Class/unregister?email=emma@mergington.edu"
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the participant was removed
        assert "emma@mergington.edu" not in activities["Programming Class"]["participants"]
    
    def test_signup_then_unregister_flow(self, client, reset_activities):
        """Test complete signup then unregister flow"""
        email = "testflow@mergington.edu"
        activity = "Science Olympiad"
        
        # Initial state - participant not registered
        assert email not in activities[activity]["participants"]
        
        # Sign up
        signup_response = client.post(f"/activities/{activity}/signup?email={email}")
        assert signup_response.status_code == status.HTTP_200_OK
        assert email in activities[activity]["participants"]
        
        # Unregister
        unregister_response = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert unregister_response.status_code == status.HTTP_200_OK
        assert email not in activities[activity]["participants"]