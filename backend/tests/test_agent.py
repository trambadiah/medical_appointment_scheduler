import pytest
from api.chat import process_chat
from utils.chat_store import get_recent_messages
from models.schemas import ChatRequest

pytestmark = pytest.mark.asyncio

async def test_complete_booking_flow():
    """
    Test a complete appointment booking conversation flow
    """
    conversation = [
        {
            "input": "I need to see the doctor",
            "expected_keywords": ["appointment", "help", "schedule"]
        },
        {
            "input": "I've been having headaches",
            "expected_keywords": ["type", "consultation", "specialty"]
        },
        {
            "input": "General consultation is fine",
            "expected_keywords": ["time", "date", "available", "schedule"]
        },
        {
            "input": "Afternoon if possible, On November 10th",
            "expected_keywords": ["available", "time", "slot"]
        },
        {
            "input": "9:00 will work",
            "expected_keywords": ["details", "name", "contact"]
        },
        {
            "input": "John Doe",
            "expected_keywords": ["phone", "number", "contact"]
        },
        {
            "input": "1234567890",
            "expected_keywords": ["email"]
        },
        {
            "input": "jd@gmail.com",
            "expected_keywords": ["confirm", "book", "appointment"]
        }
    ]
    
    session_id = None
    
    # Process each message in the conversation
    for step in conversation:
        request = ChatRequest(message=step["input"], session_id=session_id)
        response = await process_chat(request)
        
        # Update session_id after first response
        if session_id is None:
            session_id = response.get("session_id")
        
        # Verify we got a valid response
        assert response is not None
        assert "message" in response
        assert response["session_id"] == session_id
        
        # Check that response contains expected keywords
        message = response["message"].lower()
        assert any(keyword.lower() in message for keyword in step["expected_keywords"]), \
            f"Response '{message}' missing expected keywords {step['expected_keywords']}"

async def test_faq_query():
    """
    Test the FAQ query functionality
    """
    conversation = [
        {
            "input": "What are your clinic hours?",
            "expected_keywords": ["hour", "open", "time"]
        }
    ]
    
    session_id = None
    request = ChatRequest(message=conversation[0]["input"], session_id=session_id)
    response = await process_chat(request)
    
    assert response is not None
    assert "message" in response
    message = response["message"].lower()
    assert any(keyword in message for keyword in conversation[0]["expected_keywords"]), \
        f"FAQ response '{message}' missing expected keywords {conversation[0]['expected_keywords']}"

    