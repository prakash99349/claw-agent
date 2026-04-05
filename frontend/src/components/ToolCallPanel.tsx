import { useState } from "react";
import { ToolCall } from "../lib/models";
import { ChevronDown, ChevronUp } from "lucide-react";

interface Props {
  toolCall: ToolCall;
}

export default function ToolCallPanel({ toolCall }: Props) {
  const [open, setOpen] = useState(false);

  return (
    <div className="border border-emerald-700/50 rounded-lg bg-gray-900/50 text-sm font-mono overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 w-full px-4 py-3 text-left hover:bg-gray-800/50 transition-colors"
      >
        <span className="text-emerald-400">⚡</span>
        <span className="text-emerald-300 font-semibold">{toolCall.name}</span>
        <span className="text-gray-500 ml-auto">
          {open ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
        </span>
      </button>
      {open && toolCall.output && (
        <div className="border-t border-emerald-900/50 px-4 py-3">
          <pre className="text-gray-300 whitespace-pre-wrap break-all max-h-64 overflow-y-auto">
            {toolCall.output}
          </pre>
        </div>
      )}
    </div>
  );
}