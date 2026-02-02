import json
import os
import threading

MEMORY_FILE = "chat_memory.json"
MEMORY = {}
LOCK = threading.Lock()

def load_memory():
    global MEMORY
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            MEMORY = json.load(f)

def save_memory():
    with LOCK:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(MEMORY, f, indent=2)

def get_session(session_id: str):
    with LOCK:
        if session_id not in MEMORY:
            MEMORY[session_id] = []
        return MEMORY[session_id]

def update_session(session_id: str, messages: list):
    with LOCK:
        MEMORY[session_id] = messages
        save_memory()
