import { useState } from "react";
import { ChevronDown } from "lucide-react";

const MODELS = [
  { group: "Anthropic", models: ["claude-opus-4-6", "claude-sonnet-4-6"] },
  { group: "OpenAI", models: ["gpt-4o", "o3"] },
  { group: "NVIDIA NIM", models: ["meta/llama-3.1-405b-instruct", "nvidia/llama-3.1-nemotron-70b-instruct", "mistralai/mistral-large", "meta/codellama-70b"] },
  { group: "Gemini", models: ["gemini-2.0-flash", "gemini-2.0-pro"] },
];

interface Props {
  value: string;
  onChange: (model: string) => void;
}

export default function ModelSelector({ value, onChange }: Props) {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative border-b border-gray-800 px-4 py-2">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 text-sm text-gray-300 hover:text-white"
      >
        <span className="text-xs text-gray-500 uppercase tracking-wider">Model:</span>
        <span className="font-mono text-blue-400">{value}</span>
        <ChevronDown size={14} />
      </button>

      {open && (
        <div className="absolute top-full left-0 mt-1 bg-gray-900 border border-gray-700 rounded-lg shadow-xl z-50 min-w-64">
          {MODELS.map((group) => (
            <div key={group.group}>
              <div className="px-3 py-1.5 text-xs text-gray-500 uppercase tracking-wider bg-gray-950">{group.group}</div>
              {group.models.map((m) => (
                <button
                  key={m}
                  onClick={() => { onChange(m); setOpen(false); }}
                  className={`w-full text-left px-3 py-2 text-sm font-mono hover:bg-gray-800 ${m === value ? "text-blue-400 bg-gray-800" : "text-gray-300"}`}
                >
                  {m}
                </button>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}