import os
from typing import Dict, Any

ALLOWED_DIRS = ["/home/workspace", "/tmp"]

def read_file(path: str, source: str = "local") -> Dict[str, Any]:
    if source == "github":
        from github.client import GitHubClient
        client = GitHubClient()
        import asyncio
        try:
            result = asyncio.get_event_loop().run_until_complete(client.get_file(path))
            return result
        except Exception as e:
            return {"error": str(e)}
    else:
        for allowed in ALLOWED_DIRS:
            if path.startswith(allowed) or path.startswith("/home/workspace"):
                break
        if not any(path.startswith(allowed) for allowed in ["/home/workspace", "/tmp", "/app"]):
            return {"error": "Path not in allowed directories"}
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                return {"content": f.read(), "path": path}
        except Exception as e:
            return {"error": str(e)}

def write_file(path: str, content: str, source: str = "local", commit_message: str = None) -> Dict[str, Any]:
    if source == "github":
        from github.client import GitHubClient
        client = GitHubClient()
        import asyncio
        try:
            # Get sha first
            existing = asyncio.get_event_loop().run_until_complete(client.get_file(path))
            sha = existing.get("sha")
        except:
            sha = None
        try:
            result = asyncio.get_event_loop().run_until_complete(
                client.write_file(path, content, commit_message or f"Update {path}", sha)
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    else:
        for allowed in ["/home/workspace", "/tmp", "/app"]:
            if path.startswith(allowed):
                break
        else:
            return {"error": "Path not in allowed directories"}
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"path": path, "content": content}
        except Exception as e:
            return {"error": str(e)}