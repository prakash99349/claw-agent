const BASE = "/api";

export async function listSessions() {
  const res = await fetch(`${BASE}/sessions`);
  return res.json();
}

export async function createSession(model?: string, repo?: string) {
  const res = await fetch(`${BASE}/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ model, repo }),
  });
  return res.json();
}

export async function deleteSession(sessionId: string) {
  await fetch(`${BASE}/sessions/${sessionId}`, { method: "DELETE" });
}

export async function listModels() {
  const res = await fetch(`${BASE}/models`);
  return res.json();
}

export async function getRepoTree(branch = "main") {
  const res = await fetch(`${BASE}/repo/tree?branch=${branch}`);
  return res.json();
}

export async function getRepoFile(path: string) {
  const res = await fetch(`${BASE}/repo/file?path=${encodeURIComponent(path)}`);
  return res.json();
}

export function streamChat(
  sessionId: string,
  message: string,
  model: string,
  onChunk: (text: string) => void,
  onTool: (content: string) => void,
  onDone: () => void
) {
  return fetch(`${BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message, model }),
  }).then((res) => {
    const reader = res.body!.getReader();
    const decoder = new TextDecoder();
    const process = () => {
      reader.read().then(({ done, value }) => {
        if (done) { onDone(); return; }
        const lines = decoder.decode(value).split("\n");
        for (const line of lines) {
          if (line.startsWith("data: ") && !line.includes("[DONE]")) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.type === "text") onChunk(data.content);
              else if (data.type === "tool") onTool(data.content);
            } catch {}
          }
        }
        process();
      });
    };
    process();
  });
}