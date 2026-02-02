import requests
from pathlib import Path

p = Path("test_upload_dummy.pdf")
p.write_bytes(b"%PDF-1.4\n%Dummy PDF\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF")

files = {"file": ("test_upload_dummy.pdf", open(p, 'rb'), "application/pdf")}

try:
    r = requests.post("http://localhost:8000/upload_pdf", files=files, timeout=10)
    print("STATUS:", r.status_code)
    print(r.text)
except Exception as e:
    print("Error:", e)
