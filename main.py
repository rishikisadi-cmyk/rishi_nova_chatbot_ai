from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langsmith import traceable
from contextlib import asynccontextmanager
from src.db.database import engine, Base
from src.memory.session_store import load_memory, get_session, save_session, get_pdf_text



import os
import asyncio

# Load env variables
load_dotenv()
load_memory()

# Lifespan for DB startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database connected & tables ready")
    yield
    await engine.dispose()
    print("🛑 Database connection closed")

# Attach lifespan
app = FastAPI(lifespan=lifespan)

# Register routes
from src.routes.pdf_route import router as pdf_router
app.include_router(pdf_router)

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    streaming=True
)

# Main Streaming Chat Endpoint
@traceable(run_type="llm", name="Nova Chat Stream")
@app.post("/chat")
async def chat(request: Request):

    data = await request.json()
    prompt = data["message"]
    session_id = data["session_id"]

    # 1️⃣ Load chat history
    history = get_session(session_id)

    # 2️⃣ Store user message
    history.append({"role": "user", "content": prompt})

    # 3️⃣ Build full prompt
    # Attach PDF context (if any) to the prompt to enable PDF QA
    pdf_text = get_pdf_text(session_id)
    pdf_context = ""
    if pdf_text:
        # limit context length to avoid huge prompts
        pdf_context = f"PDF CONTEXT:\n{pdf_text[:3000]}\n\n"

    full_prompt = ""
    for msg in history:
        full_prompt += f"{msg['role']}: {msg['content']}\n"

    full_prompt = pdf_context + full_prompt

    # 4️⃣ Stream AI response
    async def event_generator():
        ai_reply = ""

        async for chunk in llm.astream(full_prompt):
            if chunk.content:
                ai_reply += chunk.content
                yield {
                    "event": "message",
                    "data": chunk.content
                }
                await asyncio.sleep(0.01)

        # 5️⃣ Save AI response to DB
        history.append({"role": "assistant", "content": ai_reply})
        save_session(session_id, history)


    return EventSourceResponse(event_generator())
