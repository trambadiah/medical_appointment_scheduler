"""
In-memory chat storage.

Stores chat messages per session as a list of dictionaries:
[
    {"role": "user", "message": "Hello"},
    {"role": "agent", "message": "Hi there!"}
]
"""

import uuid
from typing import Dict, List, Optional

CHAT_SESSIONS: Dict[str, List[Dict[str, str]]] = {}


def create_session(session_id: Optional[str] = None) -> str:
    """
    Create a new chat session or reuse an existing one.
    """
    if session_id and session_id in CHAT_SESSIONS:
        return session_id

    if session_id and session_id not in CHAT_SESSIONS:
        CHAT_SESSIONS[session_id] = []
        return session_id

    new_session_id = str(uuid.uuid4())
    CHAT_SESSIONS[new_session_id] = []
    return new_session_id


def add_message(session_id: str, role: str, message: str) -> None:
    """Append a message to a session's chat memory."""
    if session_id not in CHAT_SESSIONS:
        CHAT_SESSIONS[session_id] = []
    CHAT_SESSIONS[session_id].append({"role": role.lower(), "message": message.strip()})


def get_chat(session_id: str) -> List[Dict[str, str]]:
    """Return the full chat history for a given session."""
    return CHAT_SESSIONS.get(session_id, [])


def get_recent_messages(session_id: str, n: int = 10) -> List[Dict[str, str]]:
    """Return the last n messages for context (default: 10)."""
    history = CHAT_SESSIONS.get(session_id, [])
    return history[-n:]


def clear_chat(session_id: str) -> None:
    """Clear all messages for a given session."""
    if session_id in CHAT_SESSIONS:
        CHAT_SESSIONS[session_id] = []


def list_sessions() -> List[str]:
    """List all active session IDs."""
    return list(CHAT_SESSIONS.keys())


def delete_session(session_id: str) -> None:
    """Completely remove a chat session from memory."""
    if session_id in CHAT_SESSIONS:
        del CHAT_SESSIONS[session_id]

