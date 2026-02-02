from pypdf import PdfReader
from io import BytesIO


def extract_pdf_text(file_data):
    """Extract text from PDF bytes or a file-like object.

    Accepts either bytes (common when using UploadFile.read()) or
    a file-like object.
    """
    if isinstance(file_data, (bytes, bytearray)):
        reader = PdfReader(BytesIO(file_data))
    else:
        reader = PdfReader(file_data)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def summarize_text(text, max_sentences: int = 3):
    """Produce a lightweight summary by taking the first few sentences.

    This is a simple heuristic summary to avoid adding heavy dependencies.
    """
    import re

    if not text:
        return ""

    # Split into sentences (basic rule)
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return text[:500]

    summary = " ".join(sentences[:max_sentences])
    return summary
