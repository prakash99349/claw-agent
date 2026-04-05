from fastapi import APIRouter

router = APIRouter()

MODELS = [
    {"group": "Anthropic", "models": ["claude-opus-4-6", "claude-sonnet-4-6"]},
    {"group": "OpenAI", "models": ["gpt-4o", "o3"]},
    {"group": "NVIDIA NIM", "models": ["meta/llama-3.1-405b-instruct", "nvidia/llama-3.1-nemotron-70b-instruct", "mistralai/mistral-large", "meta/codellama-70b"]},
    {"group": "Gemini", "models": ["gemini-2.0-flash", "gemini-2.0-pro"]},
]

@router.get("/models")
async def list_models():
    return {"models": MODELS}