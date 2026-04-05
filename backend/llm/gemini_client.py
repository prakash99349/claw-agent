try:
    from google import genai
    from google.genai import types
    USE_NEW = True
except ImportError:
    import google.generativeai as genai
    USE_NEW = False
from typing import AsyncGenerator
from llm.chunk import LLMChunk
from config import settings

class GeminiClient:
    def __init__(self):
        if USE_NEW:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        else:
            genai.configure(api_key=settings.GEMINI_API_KEY)

    async def stream(self, model: str, messages: list, tools: list) -> AsyncGenerator[LLMChunk, None]:
        model_name = model if model.startswith("gemini") else "gemini-2.0-flash"
        try:
            if USE_NEW:
                contents = []
                for msg in messages:
                    role = "user" if msg["role"] in ("system", "user") else "model"
                    contents.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))
                config = types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=4096,
                )
                if tools:
                    config.tools = [types.Tool(function_declarations=[
                        {"name": t["name"], "description": t["description"], "parameters": t["input_schema"]}
                        for t in tools
                    ])]
                response = await self.client.aio.models.generate_content_stream(
                    model=model_name, contents=contents, config=config
                )
                async for chunk in response:
                    for part in chunk.candidates[0].content.parts:
                        if part.text:
                            yield LLMChunk(type="text", content=part.text)
                        elif part.function_call:
                            fc = part.function_call
                            args = {k: v for k, v in fc.args.items()} if hasattr(fc.args, 'items') else {}
                            yield LLMChunk(type="tool_use", name=fc.name, input=str(args), id="")
            else:
                gemini_model = genai.GenerativeModel(model_name)
                contents = []
                for msg in messages:
                    if msg["role"] == "system":
                        contents.append({"role": "user", "parts": [msg["content"]]})
                    else:
                        contents.append({"role": msg["role"], "parts": [msg["content"]]})
                config = {"temperature": 0.2, "max_output_tokens": 4096}
                if tools:
                    tool_collection = genai.protos.Tool(function_declarations=[
                        {"name": t["name"], "description": t["description"], "parameters": t["input_schema"]}
                        for t in tools
                    ])
                    gemini_model = genai.GenerativeModel(model_name, tools=[tool_collection])
                response = await gemini_model.generate_content_async(content=contents, generation_config=config, stream=True)
                async for chunk in response:
                    for part in chunk.parts:
                        if part.text:
                            yield LLMChunk(type="text", content=part.text)
                        elif part.function_call:
                            fc = part.function_call
                            yield LLMChunk(type="tool_use", name=fc.name, input=str(dict(fc.args)), id="")
        except Exception as e:
            yield LLMChunk(type="text", content=f"[Error: {str(e)}]")
