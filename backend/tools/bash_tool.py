import asyncio
from typing import Dict, Any

BLOCKED = ["rm -rf /", "sudo rm", ":(){ :|:& };:", "curl http://", "wget http://"]

async def run_bash(command: str, timeout_seconds: int = 30) -> Dict[str, Any]:
    for blocked in BLOCKED:
        if blocked in command:
            return {"error": f"Blocked command: {blocked}"}
    try:
        result = await asyncio.wait_for(
            asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            ),
            timeout=timeout_seconds
        )
        stdout, stderr = await result.communicate()
        return {
            "stdout": stdout.decode("utf-8", errors="replace"),
            "stderr": stderr.decode("utf-8", errors="replace"),
            "returncode": result.returncode
        }
    except asyncio.TimeoutError:
        return {"error": f"Command timed out after {timeout_seconds}s"}
    except Exception as e:
        return {"error": str(e)}