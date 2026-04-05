from openai import AsyncOpenAI
from typing import AsyncGenerator
from llm.router import LLMChunk
from config import settings

class OpenAIClient:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def stream(self, model: str, messages: list, tools: list) -> AsyncGenerator[LLMChunk, None]:
        kwargs = {
            "model": model,
            "messages": messages,
            "stream": True,
            "max_tokens": 4096,
            "temperature": 0.2,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
        try:
            response = await self.client.chat.completions.create(**kwargs)
            async for chunk in response:
                delta = chunk.choices[0].delta
                if delta.content:
                    yield LLMChunk(type="text", content=delta.content)
                if delta.tool_calls:
                    for tc in delta.tool_calls:
                        yield LLMChunk(
                            type="tool_use",
                            name=tc.function.name,
                            input=tc.function.arguments,
                            id=tc.id or ""
                        )
        except Exception as e:
            yield LLMChunk(type="text", content=f"[Error: {str(e)}]")
