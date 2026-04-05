from fastapi import APIRouter
from pydantic import BaseModel
from db.session_store import get_session, create_session, get_sessions, delete_session

router = APIRouter()

class CreateSessionRequest(BaseModel):
    model: str = None
    repo: str = None

@router.get("/sessions")
async def list_sessions():
    sessions = await get_sessions()
    return {"sessions": [{"id": s.id, "model": s.model, "repo": s.repo, "created_at": str(s.created_at), "updated_at": str(s.updated_at)} for s in sessions]}

@router.post("/sessions")
async def new_session(req: CreateSessionRequest = None):
    db_session = await create_session()
    return {"id": db_session.id, "model": db_session.model, "repo": db_session.repo, "created_at": str(db_session.created_at)}

@router.get("/sessions/{session_id}")
async def get_session_details(session_id: str):
    db_session = await get_session(session_id)
    if not db_session:
        return {"error": "Session not found"}, 404
    return {
        "id": db_session.id,
        "model": db_session.model,
        "repo": db_session.repo,
        "summary": db_session.summary,
        "created_at": str(db_session.created_at),
        "updated_at": str(db_session.updated_at),
        "turns": [{"id": t.id, "role": t.role, "content": t.content, "created_at": str(t.created_at)} for t in db_session.turns]
    }

@router.delete("/sessions/{session_id}")
async def remove_session(session_id: str):
    await delete_session(session_id)
    return {"deleted": session_id}