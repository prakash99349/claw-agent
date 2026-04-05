from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent.runtime import AgentRuntime
from agent.session import Session
from db.session_store import get_session, create_session
from tools.registry import get_tools
import json

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str = None
    message: str
    model: str = None

@router.post("/chat")
async def chat(request: ChatRequest):
    session = None
    if request.session_id:
        db_session = await get_session(request.session_id)
        if db_session:
            session = Session(
                id=db_session.id,
                model=db_session.model,
                repo=db_session.repo,
                context_summary=db_session.summary
            )
    if not session:
        db_session = await create_session()
        session = Session(id=db_session.id, model=request.model or db_session.model)

    if request.model:
        session.set_model(request.model)

    session.tools = get_tools()
    runtime = AgentRuntime(session)

    async def event_stream():
        async for chunk in runtime.run(request.message):
            if chunk.startswith("[tool:"):
                yield f"data: {json.dumps({'type': 'tool', 'content': chunk})}\n\n"
            else:
                yield f"data: {json.dumps({'type': 'text', 'content': chunk})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")