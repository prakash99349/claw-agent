from typing import AsyncGenerator
import json
from agent.prompt_builder import build_messages
from agent.session import Session
from agent.compaction import maybe_compact
from llm.router import route, LLMChunk
from tools.registry import execute_tool
from db.session_store import save_turn

class AgentRuntime:
    def __init__(self, session: Session):
        self.session = session

    async def run(self, user_message: str) -> AsyncGenerator[str, None]:
        self.session.add_turn("user", user_message)
        await maybe_compact(self.session)
        messages = build_messages(self.session)

        tool_calls = []
        text_buffer = ""

        async for chunk in route(self.session.model, messages, self.session.tools):
            if chunk.type == "text":
                text_buffer += chunk.content
                yield chunk.content
            elif chunk.type == "tool_use":
                tool_calls.append(chunk)

        if tool_calls:
            tool_results = []
            for call in tool_calls:
                inputs = {}
                try:
                    if isinstance(call.input, str):
                        inputs = json.loads(call.input) if call.input else {}
                    else:
                        inputs = call.input or {}
                except:
                    inputs = {"input": str(call.input)}
                result = await execute_tool(call.name, inputs)
                tool_results.append({"tool": call.name, "input": inputs, "output": result})
                yield f"\n[tool:{call.name}]\n{json.dumps(result, indent=2)}\n"

            messages.append({"role": "assistant", "content": text_buffer})
            messages.append({
                "role": "tool",
                "content": json.dumps([{"name": r["tool"], "result": r["output"]} for r in tool_results])
            })

            text_buffer = ""
            async for chunk in route(self.session.model, messages, []):
                if chunk.type == "text":
                    text_buffer += chunk.content
                    yield chunk.content

        await save_turn(self.session, "user", user_message)
        if text_buffer:
            await save_turn(self.session, "assistant", text_buffer)