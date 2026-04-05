"""
When session approaches the model's context limit, summarize older turns
and replace them with a compressed <context_summary> block.
"""
import tiktoken
from llm.router import route

COMPACTION_THRESHOLD = 0.75
RECENT_TURNS_TO_KEEP = 10

async def maybe_compact(session):
    token_count = count_tokens(session)
    limit = session.context_limit
    if token_count / limit < COMPACTION_THRESHOLD:
        return
    turns_to_summarize = session.recent_turns[:-RECENT_TURNS_TO_KEEP]
    if not turns_to_summarize:
        return
    summary_prompt = (
        "Summarize the following conversation in dense bullet points, "
        "preserving all key decisions, file changes, tool results, and context "
        "the agent will need to continue the task.\n\n"
        + format_turns(turns_to_summarize)
    )
    summary = ""
    async for chunk in route(session.model, [{"role":"user","content":summary_prompt}], []):
        if chunk.type == "text":
            summary += chunk.content
    session.context_summary = (session.context_summary or "") + "\n" + summary
    session.recent_turns = session.recent_turns[-RECENT_TURNS_TO_KEEP:]

def count_tokens(session) -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    all_text = " ".join(t.content for t in session.recent_turns)
    return len(enc.encode(all_text))

def format_turns(turns) -> str:
    return "\n".join(f"{t.role.upper()}: {t.content}" for t in turns)
