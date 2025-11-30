import os
import requests
import base64
import json
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "mock").lower()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def clean_markdown(text: str) -> str:
    """Remove markdown symbols like **, *, #'s etc."""
    replacements = [
        ("**", ""),
        ("*", ""),
        ("###", ""),
        ("##", ""),
        ("#", ""),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text.strip()


def call_llm(prompt: str, max_tokens: int = 600, temperature: float = 0.7) -> str:
    """Wrapper for different LLM providers."""

    # ----- MOCK -----
    if PROVIDER == "mock":
        return f"[MOCK LLM RESPONSE]\nPrompt: {prompt[:180]}..."

    # ----- OPENAI -----
    if PROVIDER == "openai":
        if not OPENAI_API_KEY:
            return "[ERROR] OPENAI_API_KEY not set"

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        resp = requests.post(url, headers=headers, json=data, timeout=60)
        resp.raise_for_status()
        raw = resp.json()["choices"][0]["message"]["content"]
        return clean_markdown(raw)

    # ----- GEMINI -----
    if PROVIDER == "gemini":
        if not GEMINI_API_KEY:
            return "[ERROR] GEMINI_API_KEY not set"

        model = "gemini-2.0-flash"
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={GEMINI_API_KEY}"

        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }

        resp = requests.post(url, headers=headers, json=data, timeout=60)
        if resp.status_code != 200:
            return f"[GEMINI API ERROR]\n{resp.text}"

        try:
            raw = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            return clean_markdown(raw)
        except Exception:
            return f"[GEMINI PARSE ERROR]\n{resp.text}"

    # ----- FALLBACK -----
    return "[ERROR] Unknown LLM provider. Set LLM_PROVIDER=mock/openai/gemini"

# -------------------------
# IMAGE GENERATION
# -------------------------
def generate_image(prompt: str):
    """
    Generates a high-resolution professional image using AI (OpenAI DALL·E 3).
    Returns raw PNG bytes (ready for DOCX/PPTX).
    """

    if PROVIDER != "openai":
        return None  # Image supported only when OpenAI provider is selected

    if not OPENAI_API_KEY:
        return None

    url = "https://api.openai.com/v1/images/generations"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": "1024x1024",
    }

    try:
        resp = requests.post(url, json=data, headers=headers, timeout=60)
        resp.raise_for_status()
        b64 = resp.json()["data"][0]["b64_json"]
        return base64.b64decode(b64)
    except Exception as e:
        print("Image generation failed:", e)
        return None
