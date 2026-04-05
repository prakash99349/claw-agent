import { useState, useCallback } from "react";
import { streamChat } from "../lib/api";

export function useStream() {
  const [chunks, setChunks] = useState<string[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);

  const stream = useCallback(
    (
      sessionId: string,
      message: string,
      model: string,
      onTool: (content: string) => void
    ) => {
      setIsStreaming(true);
      setChunks([]);
      streamChat(
        sessionId,
        message,
        model,
        (text) => setChunks((prev) => [...prev, text]),
        onTool,
        () => setIsStreaming(false)
      );
    },
    []
  );

  return { chunks, isStreaming, stream };
}