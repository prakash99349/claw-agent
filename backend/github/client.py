import httpx
import base64
from config import settings

BASE_URL = "https://api.github.com"

class GitHubClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"token {settings.GITHUB_PAT}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        self.repo = settings.GITHUB_REPO

    async def get_file(self, path: str) -> dict:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{BASE_URL}/repos/{self.repo}/contents/{path}",
                headers=self.headers
            )
            r.raise_for_status()
            data = r.json()
            content = base64.b64decode(data["content"]).decode("utf-8")
            return {"path": path, "content": content, "sha": data["sha"]}

    async def write_file(self, path: str, content: str,
                          message: str, sha: str = None) -> dict:
        payload = {
            "message": message,
            "content": base64.b64encode(content.encode()).decode(),
        }
        if sha:
            payload["sha"] = sha
        async with httpx.AsyncClient() as client:
            r = await client.put(
                f"{BASE_URL}/repos/{self.repo}/contents/{path}",
                headers=self.headers, json=payload
            )
            r.raise_for_status()
            return r.json()

    async def get_tree(self, branch: str = "main") -> list:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{BASE_URL}/repos/{self.repo}/git/trees/{branch}?recursive=1",
                headers=self.headers
            )
            r.raise_for_status()
            return r.json()["tree"]

    async def search_code(self, query: str) -> list:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{BASE_URL}/search/code",
                headers=self.headers,
                params={"q": f"{query} repo:{self.repo}"}
            )
            r.raise_for_status()
            return r.json()["items"]

    async def create_issue(self, title: str, body: str,
                            labels: list[str] = None) -> dict:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{BASE_URL}/repos/{self.repo}/issues",
                headers=self.headers,
                json={"title": title, "body": body, "labels": labels or []}
            )
            r.raise_for_status()
            return r.json()

    async def create_pull_request(self, title: str, body: str,
                                   head: str, base: str = "main") -> dict:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{BASE_URL}/repos/{self.repo}/pulls",
                headers=self.headers,
                json={"title": title, "body": body, "head": head, "base": base}
            )
            r.raise_for_status()
            return r.json()

    async def list_commits(self, path: str = None) -> list:
        async with httpx.AsyncClient() as client:
            params = {}
            if path:
                params["path"] = path
            r = await client.get(
                f"{BASE_URL}/repos/{self.repo}/commits",
                headers=self.headers, params=params
            )
            r.raise_for_status()
            return r.json()