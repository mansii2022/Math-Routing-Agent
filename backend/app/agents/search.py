from typing import List, Dict, Any
import os, json
import httpx
from app.config import settings


def _tavily_search(query: str) -> Dict[str, Any]:
    if not settings.tavily_api_key:
        return {"results": [], "provider": "tavily", "error": "TAVILY_API_KEY not set"}
    url = "https://api.tavily.com/search"
    payload = {"api_key": settings.tavily_api_key, "query": query, "max_results": 5}
    with httpx.Client(timeout=60) as client:
        r = client.post(url, json=payload)
        r.raise_for_status()
        return {"results": r.json().get("results", []), "provider": "tavily"}

def _exa_search(query: str) -> Dict[str, Any]:
    if not settings.exa_api_key:
        return {"results": [], "provider": "exa", "error": "EXA_API_KEY not set"}
    url = "https://api.exa.ai/search"
    headers = {"x-api-key": settings.exa_api_key}
    with httpx.Client(timeout=60) as client:
        r = client.post(url, headers=headers, json={"query": query, "numResults": 5})
        r.raise_for_status()
        return {"results": r.json().get("results", []), "provider": "exa"}

def _serper_search(query: str) -> Dict[str, Any]:
    if not settings.serper_api_key:
        return {"results": [], "provider": "serper", "error": "SERPER_API_KEY not set"}
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": settings.serper_api_key}
    with httpx.Client(timeout=60) as client:
        r = client.post(url, headers=headers, json={"q": query})
        r.raise_for_status()
        data = r.json()
        return {"results": data.get("organic", []), "provider": "serper"}

def _mcp_search(query: str) -> Dict[str, Any]:
    # Minimal JSON-RPC call to an MCP tool named settings.mcp_tool_name over HTTP/WebSocket gateway
    # Here we assume a generic HTTP POST endpoint for simplicity.
    if not settings.mcp_server:
        return {"results": [], "provider": "mcp", "error": "MCP_SERVER not set"}
    try:
        with httpx.Client(timeout=60) as client:
            r = client.post(settings.mcp_server, json={"method": settings.mcp_tool_name or "search", "params": {"query": query}})
            r.raise_for_status()
            return {"results": r.json().get("results", []), "provider": "mcp"}
    except Exception as e:
        return {"results": [], "provider": "mcp", "error": str(e)}

def smart_search(query: str) -> Dict[str, Any]:
    # Prefer MCP if configured, else Tavily -> Exa -> Serper
    if settings.mcp_server:
        res = _mcp_search(query)
        if res.get("results"):
            return res
    for fn in (_tavily_search, _exa_search, _serper_search):
        res = fn(query)
        if res.get("results"):
            return res
    return {"results": [], "provider": "none", "error": "no provider returned results"}
