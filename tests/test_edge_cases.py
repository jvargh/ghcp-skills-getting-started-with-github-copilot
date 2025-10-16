"""
Edge case and validation tests
"""
import pytest
from fastapi import status
from src.app import activities


class TestEdgeCases:
    """Test edge cases and validation scenarios"""
    
    def test_missing_email_parameter_signup(self, client, reset_activities):
        """Test signup without email parameter"""
        response = client.post("/activities/Chess Club/signup")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_missing_email_parameter_unregister(self, client, reset_activities):
        """Test unregister without email parameter"""
        response = client.delete("/activities/Chess Club/unregister")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_empty_email_signup(self, client, reset_activities):
        """Test signup with empty email"""
        response = client.post("/activities/Chess Club/signup?email=")
        # Should still process but with empty string
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    
    def test_activity_name_with_spaces(self, client, reset_activities):
        """Test activity names with spaces work correctly"""
        response = client.get("/activities")
        data = response.json()
        
        # Verify activities with spaces exist
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
    
    def test_case_sensitive_activity_names(self, client, reset_activities):
        """Test that activity names are case sensitive"""
        response = client.post("/activities/chess club/signup?email=test@mergington.edu")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_participant_list_integrity(self, client, reset_activities):
        """Test that participant lists maintain integrity across operations"""
        activity_name = "Drama Society"
        original_participants = activities[activity_name]["participants"].copy()
        
        # Add a participant
        new_email = "newactor@mergington.edu"
        signup_response = client.post(f"/activities/{activity_name}/signup?email={new_email}")
        assert signup_response.status_code == status.HTTP_200_OK
        
        # Verify original participants are still there
        current_participants = activities[activity_name]["participants"]
        for participant in original_participants:
            assert participant in current_participants
        assert new_email in current_participants
        
        # Remove the new participant
        unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={new_email}")
        assert unregister_response.status_code == status.HTTP_200_OK
        
        # Verify we're back to original state
        assert activities[activity_name]["participants"] == original_participants
    
    def test_multiple_rapid_signups(self, client, reset_activities):
        """Test multiple rapid signups for the same activity"""
        activity_name = "Basketball Team"
        emails = [f"player{i}@mergington.edu" for i in range(5)]
        
        # Sign up multiple participants
        for email in emails:
            response = client.post(f"/activities/{activity_name}/signup?email={email}")
            assert response.status_code == status.HTTP_200_OK
        
        # Verify all were added
        participants = activities[activity_name]["participants"]
        for email in emails:
            assert email in participants