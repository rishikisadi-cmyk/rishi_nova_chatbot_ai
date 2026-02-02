from fastapi import APIRouter
from src.handlers.chat_handler import chat_agent_handler


router = APIRouter()

@router.post("/chat")
def chat_agent_route(payload: dict):
    print("🔥 BACKEND HIT:", payload)  # DEBUG LINE
    return chat_agent_handler(
        message=payload["message"],
        session_id=payload["session_id"]
    )

    return chat_agent_handler(req.message, req.session_id)
