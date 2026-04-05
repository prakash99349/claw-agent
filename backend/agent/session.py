from dataclasses import dataclass, field
from typing import Optional, Any
import uuid
from datetime import datetime

@dataclass
class Turn:
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    tool_calls: list = field(default_factory=list)
    tool_results: list = field(default_factory=list)

@dataclass
class Session:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    model: str = "claude-sonnet-4-6"
    repo: str = "ultraworkers/claw-code"
    recent_turns: list[Turn] = field(default_factory=list)
    context_summary: Optional[str] = None
    context_limit: int = 100_000
    tools: list = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def add_turn(self, role: str, content: str, **kwargs):
        self.recent_turns.append(Turn(role=role, content=content, **kwargs))
        self.updated_at = datetime.utcnow()

    def set_model(self, model: str):
        self.model = model
        limits = {
            "claude": 200_000, "gpt-4o": 128_000,
            "o3": 200_000, "meta/": 128_000,
            "gemini-2.0-flash": 1_000_000, "gemini-2.0-pro": 2_000_000
        }
        for prefix, limit in limits.items():
            if model.startswith(prefix):
                self.context_limit = limit
                break

    def clear(self):
        self.recent_turns = []
        self.context_summary = None
