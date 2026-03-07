from __future__ import annotations

import os
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


def get_provider_from_env() -> LLMProvider | None:
    provider_name = os.getenv("ANR_LLM_PROVIDER", "").strip().lower()
    if not provider_name:
        return None

    if provider_name == "openai":
        from .openai_provider import OpenAIProvider

        return OpenAIProvider()

    if provider_name == "ollama":
        from .ollama_provider import OllamaProvider

        return OllamaProvider()

    return None
