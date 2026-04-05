from fastapi import APIRouter, Query
from github.client import GitHubClient

router = APIRouter()

@router.get("/repo/tree")
async def get_tree(branch: str = Query("main")):
    client = GitHubClient()
    try:
        tree = await client.get_tree(branch)
        return {"tree": tree, "branch": branch}
    except Exception as e:
        return {"error": str(e)}, 500

@router.get("/repo/file")
async def get_file(path: str = Query(...)):
    client = GitHubClient()
    try:
        result = await client.get_file(path)
        return result
    except Exception as e:
        return {"error": str(e)}, 500