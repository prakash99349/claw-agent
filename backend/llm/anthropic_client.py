import anthropic
from typing import AsyncGenerator
from llm.router import LLMChunk
from config import settings

class AnthropicClient:
    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def stream(self, model: str, messages: list, tools: list) -> AsyncGenerator[LLMChunk, None]:
        kwargs = {
            "model": model,
            "messages": messages,
            "max_tokens": 4096,
            "temperature": 0.2,
        }
        if tools:
            kwargs["tools"] = tools
        try:
            async with self.client.messages.stream(**kwargs) as stream:
                async for event in stream:
                    if event.type == "content_block_start":
                        if event.content_block.type == "tool_use":
                            yield LLMChunk(
                                type="tool_use",
                                name=event.content_block.name,
                                input=str(event.content_block.input),
                                id=event.content_block.id
                            )
                    elif event.type == "content_block_delta":
                        if event.delta.type == "text_delta":
                            yield LLMChunk(type="text", content=event.delta.text)
                        elif event.delta.type == "input_json_delta":
                            yield LLMChunk(type="tool_input", content=event.delta.partial_json)
                    elif event.type == "message_delta":
                        if event.delta.usage:
                            pass
        except Exception as e:
            yield LLMChunk(type="text", content=f"[Error: {str(e)}]")
