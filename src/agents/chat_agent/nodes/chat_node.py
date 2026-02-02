from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 🧠 Your chatbot's personality & rules
SYSTEM_PROMPT = """
You are Indranil's personal AI assistant.

Rules:
- Be friendly, clear, and simple in explanations
- If the user asks technical questions, explain step by step
- If you don't know something, say so honestly
- Keep answers short unless user asks for detail
- If user asks about weather, time, or tools, say you can use tools

Personality:
- Supportive
- Motivating
- Calm
"""

def chat(state):
    model = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=GROQ_API_KEY
    )

    messages = state["messages"]

    # Build conversation for model
    chat_history = [SystemMessage(content=SYSTEM_PROMPT)]

    for msg in messages:
        if msg["role"] == "user":
            chat_history.append(HumanMessage(content=msg["content"]))
        else:
            chat_history.append(AIMessage(content=msg["content"]))

    response = model.invoke(chat_history)

    return {
        "messages": messages + [
            {"role": "assistant", "content": response.content}
        ]
    }
