from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload
from db.models import Base, SessionModel, TurnModel
from config import settings
import json

engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def create_session() -> SessionModel:
    async with async_session() as session:
        s = SessionModel(id=SessionModel.__dict__.get("id", ""))
        # create new session with UUID
        from uuid import uuid4
        s = SessionModel(id=str(uuid4()))
        session.add(s)
        await session.commit()
        await session.refresh(s)
        return s

async def get_session(session_id: str) -> SessionModel:
    async with async_session() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(SessionModel).where(SessionModel.id == session_id).options(selectinload(SessionModel.turns))
        )
        return result.scalar_one_or_none()

async def get_sessions() -> list:
    async with async_session() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(SessionModel).order_by(SessionModel.updated_at.desc()).options(selectinload(SessionModel.turns))
        )
        return list(result.scalars().all())

async def save_turn(session, role: str, content: str, tool_calls: list = None, tool_results: list = None):
    async with async_session() as db:
        from uuid import uuid4
        from sqlalchemy import select
        result = await db.execute(select(SessionModel).where(SessionModel.id == session.id))
        s = result.scalar_one_or_none()
        if not s:
            s = SessionModel(id=session.id, model=session.model, repo=session.repo)
            db.add(s)
        s.updated_at = __import__("datetime").datetime.utcnow()
        turn = TurnModel(
            session_id=session.id,
            role=role,
            content=content,
            tool_calls=tool_calls,
            tool_results=tool_results
        )
        db.add(turn)
        await db.commit()

async def delete_session(session_id: str):
    async with async_session() as session:
        from sqlalchemy import delete
        await session.execute(delete(TurnModel).where(TurnModel.session_id == session_id))
        await session.execute(delete(SessionModel).where(SessionModel.id == session_id))
        await session.commit()