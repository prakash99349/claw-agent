export interface Message {
  id: string;
  role: "user" | "assistant" | "tool" | "system";
  content: string;
  toolCalls?: ToolCall[];
}

export interface ToolCall {
  name: string;
  input: Record<string, unknown>;
  output?: string;
}

export interface Session {
  id: string;
  model: string;
  repo: string;
  created_at: string;
  updated_at: string;
}

export interface ModelGroup {
  group: string;
  models: string[];
}