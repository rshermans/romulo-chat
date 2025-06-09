from typing import Any

import requests

try:
    import openai
except ImportError:  # pragma: no cover - openai is optional
    openai = None


PROVIDER_ENDPOINTS = {
    "claude": "https://api.anthropic.com/v1/complete",
    "mistral": "https://api.mistral.ai/v1/chat/completions",
    "qwen": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
}


def _post_json(url: str, headers: dict, payload: dict) -> str:
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    response.raise_for_status()
    data = response.json()
    # the exact JSON varies by provider; we return the whole payload for now
    return str(data)


def call_openai(prompt: str, api_key: str) -> str:
    if openai is None:
        raise RuntimeError("openai package not available")
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]


def call_provider(provider: str, prompt: str, api_key: str) -> str:
    if provider == "openai":
        return call_openai(prompt, api_key)
    url = PROVIDER_ENDPOINTS.get(provider)
    if not url:
        raise ValueError(f"Unknown provider: {provider}")
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"prompt": prompt}
    return _post_json(url, headers, payload)


def generate_with_llm(prompt: str, provider: str, api_key: str) -> str:
    """Generate a response using the selected LLM provider."""
    try:
        return call_provider(provider, prompt, api_key)
    except Exception:
        return f"[{provider} generation failed]"
