import { useState, useRef, useEffect } from "react";
import { useSession } from "../hooks/useSession";
import MessageBubble from "./MessageBubble";
import ToolCallPanel from "./ToolCallPanel";
import ModelSelector from "./ModelSelector";
import RepoStatusBar from "./RepoStatusBar";
import SlashCommandMenu from "./SlashCommandMenu";
import { Send, Plus, Trash2 } from "lucide-react";

const SLASH_COMMANDS = [
  { cmd: "/model", desc: "Switch LLM model" },
  { cmd: "/repo", desc: "Change GitHub repo" },
  { cmd: "/clear", desc: "Clear session history" },
  { cmd: "/history", desc: "Show turn log" },
  { cmd: "/tree", desc: "Print repo file tree" },
  { cmd: "/compact", desc: "Trigger context compaction" },
  { cmd: "/help", desc: "List all slash commands" },
];

export default function ChatWindow() {
  const { messages, toolCalls, isStreaming, sendMessage, clearMessages, newSession } = useSession();
  const [input, setInput] = useState("");
  const [model, setModel] = useState("claude-sonnet-4-6");
  const [showSlash, setShowSlash] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, toolCalls]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming) return;
    if (input.startsWith("/")) {
      handleSlashCommand(input);
      return;
    }
    sendMessage(input, model);
    setInput("");
    setShowSlash(false);
  };

  const handleSlashCommand = (cmd: string) => {
    const [command, ...args] = cmd.split(" ");
    switch (command) {
      case "/clear":
        clearMessages();
        setInput("");
        break;
      case "/model":
        if (args[0]) setModel(args[0]);
        setInput("");
        break;
      case "/new":
        newSession(model);
        setInput("");
        break;
      case "/help":
        alert(SLASH_COMMANDS.map((c) => `${c.cmd} — ${c.desc}`).join("\n"));
        setInput("");
        break;
      default:
        sendMessage(cmd, model);
        setInput("");
    }
    setShowSlash(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "/" && input === "") {
      e.preventDefault();
      setShowSlash(true);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-950 text-white">
      <RepoStatusBar />
      <ModelSelector value={model} onChange={setModel} />

      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}

        {toolCalls.length > 0 && (
          <div className="space-y-2">
            {toolCalls.map((tc, i) => (
              <ToolCallPanel key={i} toolCall={tc} />
            ))}
          </div>
        )}

        {isStreaming && (
          <div className="text-gray-400 text-sm animate-pulse">Thinking...</div>
        )}

        <div ref={bottomRef} />
      </div>

      {showSlash && (
        <SlashCommandMenu
          commands={SLASH_COMMANDS}
          onSelect={(cmd) => {
            setInput(cmd);
            setShowSlash(false);
          }}
          onClose={() => setShowSlash(false)}
        />
      )}

      <form onSubmit={handleSubmit} className="border-t border-gray-800 p-4 flex gap-2">
        <button
          type="button"
          onClick={() => newSession(model)}
          className="p-2 text-gray-400 hover:text-white"
          title="New session"
        >
          <Plus size={20} />
        </button>
        <button
          type="button"
          onClick={clearMessages}
          className="p-2 text-gray-400 hover:text-red-400"
          title="Clear"
        >
          <Trash2 size={20} />
        </button>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Message or /slash command..."
          className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
          disabled={isStreaming}
        />
        <button
          type="submit"
          disabled={!input.trim() || isStreaming}
          className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 p-2 rounded-lg"
        >
          <Send size={20} />
        </button>
      </form>
    </div>
  );
}