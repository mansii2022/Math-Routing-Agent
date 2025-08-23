# backend/app/agents/search_mcp.py
from typing import Dict, List
import os, requests

MCP_SEARCH_URL = os.environ.get("MCP_SEARCH_URL", "http://localhost:8999/search")  # replace with your MCP endpoint

def smart_search(query: str) -> Dict:
    try:
        r = requests.post(MCP_SEARCH_URL, json={"q": query, "k": 5}, timeout=10)
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])
        snippets = [item.get("snippet") or item.get("title") or "" for item in results]
        return {"ok": True, "snippets": snippets[:5]}
    except Exception as e:
        return {"ok": False, "error": str(e), "snippets": []}
