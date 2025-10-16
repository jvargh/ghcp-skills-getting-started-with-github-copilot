"""
Tests for signup functionality
"""
import pytest
from fastapi import status
from src.app import activities


class TestSignupFunctionality:
    """Test activity signup functionality"""
    
    def test_signup_success(self, client, reset_activities):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]
        
        # Verify the participant was added
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]
    
    def test_signup_duplicate_participant(self, client, reset_activities):
        """Test signup with already registered participant"""
        # Try to signup an existing participant
        response = client.post(
            "/activities/Chess Club/signup?email=michael@mergington.edu"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()
    
    def test_signup_nonexistent_activity(self, client, reset_activities):
        """Test signup for non-existent activity"""
        response = client.post(
            "/activities/Nonexistent Activity/signup?email=test@mergington.edu"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_signup_with_url_encoded_activity_name(self, client, reset_activities):
        """Test signup with URL-encoded activity name"""
        response = client.post(
            "/activities/Programming%20Class/signup?email=newcoder@mergington.edu"
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the participant was added
        assert "newcoder@mergington.edu" in activities["Programming Class"]["participants"]
    
    def test_signup_with_special_characters_in_email(self, client, reset_activities):
        """Test signup with special characters in email"""
        response = client.post(
            "/activities/Art Club/signup?email=student.name%2Btag@mergington.edu"
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the participant was added (note: + gets URL decoded to space in query params)
        participants = activities["Art Club"]["participants"]
        assert any("student.name" in p for p in participants)