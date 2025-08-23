from typing import List, Dict, Any
import os
from ..config import settings
import httpx

# Simple OpenAI Chat Completions wrapper (adjust as needed)
def llm_complete(system_prompt: str, user_prompt: str) -> str:
    if not settings.openai_api_key:
        # offline-safe fallback message
        return "LLM not configured. Please set OPENAI_API_KEY."
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {settings.openai_api_key}"}
    data = {
        "model": settings.model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
    }
    with httpx.Client(timeout=60) as client:
        r = client.post(url, headers=headers, json=data)
        r.raise_for_status()
        out = r.json()
    return out["choices"][0]["message"]["content"]
