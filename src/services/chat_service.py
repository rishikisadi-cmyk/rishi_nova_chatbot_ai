from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os

from src.services.memory_store import get_session, update_session

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY
)

def run_chat(user_input: str, session_id: str):
    history = get_session(session_id)

    messages = []
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=user_input))

    response = model.invoke(messages)

    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": response.content})

    update_session(session_id, history)

    return response.content
