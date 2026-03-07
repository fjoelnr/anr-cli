from __future__ import annotations

import json
import os
from urllib import request

from .provider import LLMProvider


class OllamaProvider(LLMProvider):
    def __init__(self) -> None:
        self.model = os.getenv("ANR_OLLAMA_MODEL", "llama3.1").strip()
        self.host = os.getenv("ANR_OLLAMA_HOST", "http://localhost:11434").rstrip("/")

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url=f"{self.host}/api/generate",
            data=data,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with request.urlopen(req, timeout=20) as response:
            body = response.read().decode("utf-8")
        parsed = json.loads(body)
        return str(parsed.get("response", "")).strip()
