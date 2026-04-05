from github.client import GitHubClient
import asyncio
from typing import Dict, Any

async def github_action(action: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    client = GitHubClient()
    params = params or {}
    try:
        if action == "get_tree":
            branch = params.get("branch", "main")
            result = await client.get_tree(branch)
            return {"tree": result}
        elif action == "search_code":
            query = params.get("query", "")
            result = await client.search_code(query)
            return {"results": result}
        elif action == "create_issue":
            result = await client.create_issue(
                title=params.get("title", ""),
                body=params.get("body", ""),
                labels=params.get("labels")
            )
            return result
        elif action == "create_pull_request":
            result = await client.create_pull_request(
                title=params.get("title", ""),
                body=params.get("body", ""),
                head=params.get("head", ""),
                base=params.get("base", "main")
            )
            return result
        elif action == "list_commits":
            result = await client.list_commits(params.get("path"))
            return {"commits": result}
        else:
            return {"error": f"Unknown action: {action}"}
    except Exception as e:
        return {"error": str(e)}