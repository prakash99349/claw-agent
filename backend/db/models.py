from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class SessionModel(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True)
    model = Column(String, nullable=False, default="claude-sonnet-4-6")
    repo = Column(String, nullable=False, default="ultraworkers/claw-code")
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    turns = relationship("TurnModel", back_populates="session", cascade="all, delete-orphan")

class TurnModel(Base):
    __tablename__ = "turns"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tool_calls = Column(JSON, nullable=True)
    tool_results = Column(JSON, nullable=True)
    token_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    session = relationship("SessionModel", back_populates="turns")