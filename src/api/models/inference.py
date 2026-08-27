"""ai inferencing"""

from __future__ import annotations
import os
import requests

from api.models.config import INFERENCE_API_KEY, INFERENCE_URL
DEFAULT_MODEL = "nvidia/nemotron-3-nano-30b-a3b"

def _get_api_key() -> str:
    key = INFERENCE_API_KEY
    if not key:
        raise RuntimeError("INFERENCE_API_KEY environment variable is not set.")
    return key

def _get_model() -> str:
    model = os.getenv("MODEL", DEFAULT_MODEL)
    return model


def generate_text(
    prompt: str,
    model: str = None,
    max_tokens: int = 900,
) -> str:
    """
    send prompt to the NVIDIA-hosted chat-completions endpoint, return generated text
    """
    api_key = _get_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model or _get_model(),
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.0,
        "top_p": 1.0,
        "stream": False,
    }

    response = requests.post(
        INFERENCE_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"inference API request failed ({response.status_code}) for URL {response.url}: {response.text}"
        )
    data = response.json()
    try:
        generated_text = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"unexpected API response structure: {data}") from exc

    return generated_text.strip()