import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Nova AI", layout="centered")
st.title("🧠 RISHI AI — Streaming PDF Chatbot")

BACKEND_URL = "http://localhost:8000"

# -------------------- SESSION SETUP --------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "last_input" not in st.session_state:
    st.session_state.last_input = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------- PDF UPLOAD --------------------
uploaded_file = st.file_uploader("📄 Upload a PDF", type="pdf")

if uploaded_file:
    try:
        with st.spinner("Uploading PDF..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post(
                f"{BACKEND_URL}/upload_pdf",
                files=files,
                data={"session_id": st.session_state.session_id},
                timeout=30
            )

        if response.status_code == 200:
            data = response.json()
            st.success(data.get("message", "PDF uploaded successfully!"))

            preview = data.get("text_preview")
            summary = data.get("summary")

            if preview:
                st.text_area("PDF Preview (first 1000 chars)", preview, height=200)

            if summary:
                st.markdown("**Summary:**")
                st.markdown(summary)
        else:
            st.error(f"❌ PDF upload failed: {response.text}")

    except Exception as e:
        st.error(f"❌ Backend not running: {e}")

# -------------------- SHOW CHAT HISTORY --------------------
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(msg)

# -------------------- CHAT INPUT --------------------
user_input = st.chat_input("Ask something about the PDF or anything else...")

if user_input and user_input != st.session_state.last_input:
    st.session_state.last_input = user_input

    # Show user message
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # -------------------- STREAMING AI RESPONSE --------------------
    
        # -------------------- STREAMING AI RESPONSE --------------------
    response_box = st.empty()
    full_text = ""

    try:
        with requests.post(
            f"{BACKEND_URL}/chat",
            json={
                "message": user_input,
                "session_id": st.session_state.session_id
            },
            stream=True,
            timeout=60
        ) as r:

            if r.status_code != 200:
                response_box.markdown(f"❌ Server error: {r.text}")
            else:
                for line in r.iter_lines():
                    if not line:
                        continue

                    decoded = line.decode().strip()

                    # Only handle actual streamed tokens
                    if decoded.startswith("data:"):
                        token = decoded.replace("data:", "").strip()
                        full_text += token + " "
                        response_box.markdown(full_text + "▌")

    except Exception as e:
        full_text = f"❌ Backend error: {e}"
        response_box.markdown(full_text)


    # Save AI reply
    st.session_state.messages.append(("assistant", full_text))
