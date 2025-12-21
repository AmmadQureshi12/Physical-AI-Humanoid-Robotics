"""
Test cases for the chatbot API
"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app


client = TestClient(app)


def test_chatbot_health():
    """Test that the chatbot API is accessible"""
    response = client.get("/api/v1/chat/capabilities")
    assert response.status_code == 200
    data = response.json()
    assert "capabilities" in data
    assert len(data["capabilities"]) > 0


@pytest.mark.parametrize("user_message,expected_type", [
    ("What is a ROS 2 node?", "explanation"),
    ("How does simulation work in robotics?", "explanation"),
    ("Show me the ROS 2 architecture diagram", "resource_link"),
    ("Where can I find the publisher example?", "resource_link"),
    ("Give me the solution to this problem", "hint"),
    ("Provide the code for this exercise", "hint"),
])
def test_chatbot_response_types(user_message, expected_type):
    """Test different types of responses from the chatbot"""
    response = client.post("/api/v1/chat", json={
        "message": user_message,
        "user_id": "test_user",
        "session_id": "test_session"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert "response" in data
    assert "message_type" in data
    assert data["message_type"] == expected_type
    assert "session_id" in data


def test_chatbot_empty_message():
    """Test handling of empty messages"""
    response = client.post("/api/v1/chat", json={
        "message": "",
        "user_id": "test_user",
        "session_id": "test_session"
    })
    
    # Should still return a response even for empty message
    assert response.status_code == 200
    data = response.json()
    assert "response" in data