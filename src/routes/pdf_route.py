from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from src.tools.pdf_tool import extract_pdf_text, summarize_text
from src.memory.session_store import set_pdf_text

router = APIRouter()


@router.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...), session_id: str = Form(...)):
    # Basic content-type validation
    content_type = (file.content_type or "").lower()
    if not content_type.startswith("application/pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type - expected PDF")

    try:
        # Read file bytes (UploadFile is async)
        data = await file.read()
        text = extract_pdf_text(data)
        # Save extracted text to the user's session so the chat endpoint can use it
        try:
            set_pdf_text(session_id, text)
        except Exception:
            # non-fatal for the upload; still return parsed text/summary
            pass

        summary = summarize_text(text, max_sentences=4)
        return {
            "message": "PDF processed successfully",
            "text_preview": text[:1000],
            "summary": summary
        }
    except Exception as e:
        # Return a clear client error instead of 500
        raise HTTPException(status_code=400, detail=f"Failed to process PDF: {e}")
