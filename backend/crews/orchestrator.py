import json
import os
from typing import Any, Dict, Optional
from urllib import error, request

from config import settings


def _json_post(url: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers=headers or {}, method="POST")
    with request.urlopen(req, timeout=30) as response:
        body = response.read().decode("utf-8")
        if not body:
            return {}
        return json.loads(body)


def generate_llm_response(prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
    provider = settings.LLM_PROVIDER.lower()

    if provider == "gemini" and settings.GEMINI_API_KEY:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": f"{system or 'You are Apex Executive'}\n\n{prompt}"}]}],
            "generationConfig": {"temperature": 0.4},
        }
        try:
            result = _json_post(url, payload)
            text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text")
            if text:
                return {"provider": "gemini", "text": text, "live": True}
        except Exception:
            pass

    if provider == "groq" and settings.GROQ_API_KEY:
        url = "https://api.groq.com/openai/v1/chat/completions"
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": system or "You are Apex Executive, the CEO command intelligence layer."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.4,
        }
        headers = {"Authorization": f"Bearer {settings.GROQ_API_KEY}", "Content-Type": "application/json"}
        try:
            result = _json_post(url, payload, headers)
            text = result.get("choices", [{}])[0].get("message", {}).get("content")
            if text:
                return {"provider": "groq", "text": text, "live": True}
        except Exception:
            pass

    if provider == "openrouter" and settings.OPENROUTER_API_KEY:
        url = "https://openrouter.ai/api/v1/chat/completions"
        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system or "You are Apex Executive, the CEO command intelligence layer."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.4,
        }
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/apptesting237/apex-executive",
            "X-Title": "Apex Executive",
        }
        try:
            result = _json_post(url, payload, headers)
            text = result.get("choices", [{}])[0].get("message", {}).get("content")
            if text:
                return {"provider": "openrouter", "text": text, "live": True}
        except Exception:
            pass

    if settings.OLLAMA_BASE_URL:
        url = f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/generate"
        payload = {
            "model": "llama3.1",
            "prompt": f"{system or 'You are Apex Executive'}\n\n{prompt}",
            "stream": False,
        }
        try:
            result = _json_post(url, payload)
            text = result.get("response")
            if text:
                return {"provider": "ollama", "text": text, "live": True}
        except Exception:
            pass

    return {
        "provider": "local",
        "text": "Local executive intelligence is active. Add a real LLM provider key to enable live generation.",
        "live": False,
    }
