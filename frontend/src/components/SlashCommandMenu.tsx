import { useState, useEffect } from "react";

interface Command {
  cmd: string;
  desc: string;
}

interface Props {
  commands: Command[];
  onSelect: (cmd: string) => void;
  onClose: () => void;
}

export default function SlashCommandMenu({ commands, onSelect, onClose }: Props) {
  const [filter, setFilter] = useState("");

  const filtered = commands.filter(
    (c) => c.cmd.toLowerCase().includes(filter.toLowerCase()) ||
           c.desc.toLowerCase().includes(filter.toLowerCase())
  );

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div className="absolute bottom-20 left-1/2 -translate-x-1/2 w-80 bg-gray-900 border border-gray-700 rounded-lg shadow-xl z-50">
      <div className="p-2 border-b border-gray-700">
        <input
          type="text"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="Filter commands..."
          className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-1.5 text-sm text-white placeholder-gray-500 focus:outline-none"
          autoFocus
        />
      </div>
      <div className="max-h-64 overflow-y-auto py-1">
        {filtered.map((c) => (
          <button
            key={c.cmd}
            onClick={() => onSelect(c.cmd)}
            className="w-full text-left px-4 py-2 hover:bg-gray-800 flex justify-between items-center"
          >
            <span className="font-mono text-blue-400 text-sm">{c.cmd}</span>
            <span className="text-gray-500 text-xs">{c.desc}</span>
          </button>
        ))}
        {filtered.length === 0 && (
          <div className="px-4 py-2 text-gray-500 text-sm">No commands found</div>
        )}
      </div>
    </div>
  );
}