import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def web_search(query: str):
    if not SERPAPI_KEY:
        return "❌ SERPAPI_KEY missing in .env file"

    params = {
        "q": query,
        "engine": "google",
        "api_key": SERPAPI_KEY
    }

    try:
        res = requests.get("https://serpapi.com/search", params=params, timeout=10)
        data = res.json()
        print("🔍 RAW SERPAPI RESPONSE:\n", data)

    except Exception as e:
        return f"❌ Search failed: {e}"

    results_text = []

    # Try organic results first
    if "organic_results" in data:
        for i, item in enumerate(data["organic_results"][:5], start=1):
            title = item.get("title", "No title")
            snippet = item.get("snippet", "No description")
            link = item.get("link", "")
            results_text.append(f"{i}. {title}\n{snippet}\n{link}\n")

    # Fallback to news results
    elif "news_results" in data:
        for i, item in enumerate(data["news_results"][:5], start=1):
            title = item.get("title", "No title")
            snippet = item.get("snippet", "No description")
            link = item.get("link", "")
            results_text.append(f"{i}. {title}\n{snippet}\n{link}\n")

    # Fallback to answer box
    elif "answer_box" in data:
        answer = data["answer_box"].get("answer", "No direct answer found")
        return f"📌 Direct Answer:\n{answer}"

    else:
        return "❌ No results found (API responded but no searchable data)"

    return "\n".join(results_text)
