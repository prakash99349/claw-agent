"""
Dispatches to the correct provider based on model string prefix.
All providers return a unified async generator of LLMChunk objects.
"""
from typing import AsyncGenerator, Any
from dataclasses import dataclass
from llm.chunk import LLMChunk
from llm.anthropic_client import AnthropicClient
from llm.openai_client import OpenAIClient
from llm.nvidia_client import NvidiaClient
from llm.gemini_client import GeminiClient

PROVIDER_MAP = {
    "claude":  AnthropicClient,
    "gpt":     OpenAIClient,
    "o1":      OpenAIClient,
    "o3":      OpenAIClient,
    "meta/":   NvidiaClient,
    "nvidia/": NvidiaClient,
    "mistral": NvidiaClient,
    "gemini":  GeminiClient,
}

def get_provider(model: str):
    model_lower = model.lower()
    for prefix, client_class in PROVIDER_MAP.items():
        if model_lower.startswith(prefix):
            return client_class()
    # default to OpenAI
    return OpenAIClient()

async def route(model: str, messages: list, tools: list) -> AsyncGenerator[LLMChunk, None]:
    provider = get_provider(model)
    async for chunk in provider.stream(model, messages, tools):
        yield chunk
