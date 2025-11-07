from fastapi import APIRouter
from models.schemas import ChatRequest
from utils import chat_store
from agent.scheduling_agent import run_agent

router = APIRouter()


@router.post("/chat")
async def process_chat(request: ChatRequest):
    """
    Process a chat message within a session.
    """
    
    session_id = chat_store.create_session(request.session_id)

    chat_store.add_message(session_id, "user", request.message)
    
    return run_agent(session_id)
    
    
