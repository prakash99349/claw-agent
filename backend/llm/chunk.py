from dataclasses import dataclass, field


@dataclass
class LLMChunk:
    type: str
    content: str = ""
    name: str = ""
    input: str = ""
    id: str = ""
