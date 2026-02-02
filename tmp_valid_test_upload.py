from pypdf import PdfWriter
import requests
from io import BytesIO

# Create a minimal valid PDF in memory
writer = PdfWriter()
writer.add_blank_page(width=595, height=842)  # A4 size
buf = BytesIO()
writer.write(buf)
buf.seek(0)

files = {"file": ("valid_test.pdf", buf, "application/pdf")}

try:
    r = requests.post("http://localhost:8000/upload_pdf", files=files, timeout=10)
    print("STATUS:", r.status_code)
    print(r.text)
except Exception as e:
    print("Error:", e)
