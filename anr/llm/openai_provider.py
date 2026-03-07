from __future__ import annotations

import json
import os
from urllib import request

from .provider import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self) -> None:
        self.api_key = os.getenv("ANR_API_KEY", "").strip()
        self.model = os.getenv("ANR_OPENAI_MODEL", "gpt-4o-mini").strip()
        self.base_url = os.getenv("ANR_OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("ANR_API_KEY is required for OpenAI provider.")

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You suggest concise repository refactor improvements."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url=f"{self.base_url}/chat/completions",
            data=data,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        with request.urlopen(req, timeout=20) as response:
            body = response.read().decode("utf-8")
        parsed = json.loads(body)
        return parsed["choices"][0]["message"]["content"].strip()
