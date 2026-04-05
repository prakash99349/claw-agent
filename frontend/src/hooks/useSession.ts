import { useState, useEffect, useCallback, useRef } from "react";
import { Message, ToolCall } from "../lib/models";
import { listSessions, createSession, deleteSession as apiDeleteSession } from "../lib/api";
import { streamChat } from "../lib/api";

export function useSession() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [toolCalls, setToolCalls] = useState<ToolCall[]>([]);
  const modelRef = useRef("claude-sonnet-4-6");

  useEffect(() => {
    listSessions().then(async (data) => {
      if (data.sessions?.length > 0) {
        setSessionId(data.sessions[0].id);
      } else {
        const s = await createSession();
        setSessionId(s.id);
      }
    });
  }, []);

  const sendMessage = useCallback(
    async (content: string, model: string) => {
      if (!sessionId) return;
      modelRef.current = model;
      const userMsg: Message = {
        id: Date.now().toString(),
        role: "user",
        content,
      };
      setMessages((prev) => [...prev, userMsg]);
      setIsStreaming(true);
      setToolCalls([]);

      let assistantContent = "";
      const assistantId = (Date.now() + 1).toString();

      streamChat(
        sessionId,
        content,
        model,
        (text) => {
          assistantContent += text;
          setMessages((prev) => {
            const existing = prev.find((m) => m.id === assistantId);
            if (existing) {
              return prev.map((m) =>
                m.id === assistantId ? { ...m, content: assistantContent } : m
              );
            }
            return [...prev, { id: assistantId, role: "assistant" as const, content: text }];
          });
        },
        (toolContent) => {
          try {
            const match = toolContent.match(/\[tool:(\w+)\]\n([\s\S]*?)(?=\n\[tool:|$)/);
            if (match) {
              const toolCall: ToolCall = {
                name: match[1],
                input: {},
                output: match[2]?.trim(),
              };
              setToolCalls((prev) => [...prev, toolCall]);
            }
          } catch {}
        },
        () => {
          setIsStreaming(false);
          setToolCalls([]);
        }
      );
    },
    [sessionId]
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  const switchSession = useCallback(async (newSessionId: string) => {
    setSessionId(newSessionId);
    setMessages([]);
    setToolCalls([]);
  }, []);

  const newSession = useCallback(async (model?: string) => {
    const s = await createSession(model);
    setSessionId(s.id);
    setMessages([]);
    setToolCalls([]);
    return s.id;
  }, []);

  const deleteSession = useCallback(async (id: string) => {
    await apiDeleteSession(id);
    if (sessionId === id) {
      const data = await listSessions();
      if (data.sessions?.length > 0) {
        setSessionId(data.sessions[0].id);
      } else {
        const s = await createSession();
        setSessionId(s.id);
      }
      setMessages([]);
    }
  }, [sessionId]);

  return {
    messages,
    toolCalls,
    isStreaming,
    sessionId,
    sendMessage,
    clearMessages,
    switchSession,
    newSession,
    deleteSession,
  };
}