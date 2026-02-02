import re
from src.tools.system_tools import get_current_time
from src.tools.weather_tool import get_weather
from src.tools.web_search import web_search
from src.memory.session_store import get_session, save_session
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)
def detect_tool(message):
    msg = message.lower()

    # Time
    if re.search(r"\b(time|current time)\b", msg):
        return ("time", None)

    # Weather
    match_weather = re.search(r"weather in ([a-zA-Z\s]+)", msg)
    if match_weather:
        return ("weather", match_weather.group(1).strip())

    # Web Search
    if re.search(r"\b(search|find|web search)\b", msg):
        return ("search", msg)

    return (None, None)


def chat_agent_handler(message: str, session_id: str):
    session = get_session(session_id)
    history = session["history"]
    stored_city = session.get("city", None)

    tool, value = detect_tool(message)

    if tool == "time":
        return {"response": f"🕒 Current time is {get_current_time()}"}

    if tool == "weather":
        if value:
            session["city"] = value
            save_session(session_id, session)
        if not session["city"]:
            return {"response": "Which city?"}
        return {"response": get_weather(session["city"])}

    if tool == "search":
        search_results = web_search(value)
        return {"response": f"🔎 Search results for \"{value}\":\n{search_results}"}

    # Normal AI
    history.append({"role": "user", "content": message})
    ai_response = model.invoke(history)
    reply = ai_response.content
    history.append({"role": "assistant", "content": reply})

    session["history"] = history
    save_session(session_id, session)

    return {"response": reply}
