from tools.bash_tool import run_bash
from tools.file_tool import read_file, write_file
from tools.github_tool import github_action
from tools.search_tool import web_search
import json

TOOL_MANIFEST = [
    {
        "name": "bash",
        "description": (
            "Execute a shell command in a sandboxed environment. "
            "Use for: building code, running tests, grep, ls, file inspection, "
            "git operations, running Python/Node scripts."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The shell command to execute."},
                "timeout_seconds": {"type": "integer", "description": "Max execution time. Default 30.", "default": 30}
            },
            "required": ["command"]
        }
    },
    {
        "name": "read_file",
        "description": (
            "Read a file's content. Source can be 'local' (filesystem) "
            "or 'github' (from the connected repo)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path."},
                "source": {"type": "string", "enum": ["local", "github"], "default": "github"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": (
            "Write or update a file. If source is 'github', creates a commit. "
            "Always provide a clear commit_message for GitHub writes."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"},
                "source": {"type": "string", "enum": ["local", "github"], "default": "local"},
                "commit_message": {"type": "string", "description": "Required when source is 'github'."}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "github",
        "description": (
            "Perform GitHub operations: get_tree, search_code, create_issue, "
            "create_pull_request, list_commits."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["get_tree", "search_code", "create_issue", "create_pull_request", "list_commits"]},
                "params": {"type": "object", "description": "Action-specific parameters."}
            },
            "required": ["action"]
        }
    },
    {
        "name": "web_search",
        "description": (
            "Search the web for documentation, error messages, or current information. "
            "Use when you need info beyond the repo or your training data."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query (3-8 words)."}
            },
            "required": ["query"]
        }
    }
]

TOOL_EXECUTORS = {
    "bash":       run_bash,
    "read_file":  read_file,
    "write_file": write_file,
    "github":     github_action,
    "web_search": web_search,
}

async def execute_tool(name: str, inputs: dict) -> dict:
    executor = TOOL_EXECUTORS.get(name)
    if not executor:
        return {"error": f"Unknown tool: {name}"}
    try:
        return await executor(**inputs)
    except Exception as e:
        return {"error": str(e), "tool": name}

def get_tools():
    return TOOL_MANIFEST