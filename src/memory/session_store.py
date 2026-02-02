import json
import os

MEMORY_FILE = "chat_memory.json"
# sessions maps session_id -> {"messages": [...], "pdf_text": "..."}
sessions = {}


def load_memory():
    global sessions
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)

            # Backwards-compat: raw may have been session_id -> [messages]
            for k, v in raw.items():
                if isinstance(v, list):
                    sessions[k] = {"messages": v, "pdf_text": ""}
                elif isinstance(v, dict):
                    # Already new format
                    sessions[k] = {"messages": v.get("messages", []), "pdf_text": v.get("pdf_text", "")}


def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, indent=2)


def get_session(session_id):
    entry = sessions.get(session_id)
    if not entry:
        return []
    return entry.get("messages", [])


def save_session(session_id, messages):
    entry = sessions.get(session_id, {"messages": [], "pdf_text": ""})
    entry["messages"] = messages
    sessions[session_id] = entry
    save_memory()


def set_pdf_text(session_id, text):
    entry = sessions.get(session_id, {"messages": [], "pdf_text": ""})
    entry["pdf_text"] = text
    sessions[session_id] = entry
    save_memory()


def get_pdf_text(session_id):
    entry = sessions.get(session_id)
    if not entry:
        return ""
    return entry.get("pdf_text", "")
