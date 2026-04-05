import httpx
from typing import Dict, Any

async def web_search(query: str) -> Dict[str, Any]:
    try:
        async with httpx.AsyncClient() as client:
            # Using DuckDuckGo HTML as a simple search endpoint
            response = await client.get(
                "https://html.duckduckgo.com/html/",
                params={"q": query},
                timeout=10.0
            )
            return {"results": response.text[:2000]}
    except Exception as e:
        return {"error": str(e)}