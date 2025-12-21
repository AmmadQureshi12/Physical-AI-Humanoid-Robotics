"""
Chatbot API routes for the educational chatbot feature
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
import os
import logging
from datetime import datetime

from src.services.chat_service import ChatService

router = APIRouter()
logger = logging.getLogger(__name__)

# Models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = datetime.now()


class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    context: Optional[str] = None  # Chapter or section context


class ChatResponse(BaseModel):
    response: str
    message_type: str  # 'hint', 'explanation', 'resource_link'
    session_id: str
    timestamp: datetime = datetime.now()


# Initialize chat service
chat_service = ChatService()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint for the educational chatbot
    """
    try:
        # Use the chat service to get a response
        response_text, message_type = await chat_service.get_response(
            user_message=request.message,
            context=request.context,
            user_id=request.user_id,
            session_id=request.session_id
        )

        # Return the response
        return ChatResponse(
            response=response_text,
            message_type=message_type,
            session_id=request.session_id or "new_session",  # This should be updated by the service
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/chat/capabilities")
async def get_capabilities():
    """
    Get the capabilities of the chatbot
    """
    return {
        "capabilities": [
            "Answer questions about AI-Humanoid Robotics curriculum",
            "Provide exercise hints without full solutions",
            "Navigate to relevant resources and diagrams",
            "Maintain conversation context"
        ]
    }