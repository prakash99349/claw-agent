import { GitBranch, Github } from "lucide-react";

export default function RepoStatusBar() {
  return (
    <div className="flex items-center justify-between px-4 py-2 border-b border-gray-800 text-xs">
      <div className="flex items-center gap-2 text-gray-400">
        <Github size={14} />
        <span>ultraworkers/claw-code</span>
        <span className="text-gray-600">·</span>
        <GitBranch size={12} />
        <span className="text-gray-500">main</span>
      </div>
      <div className="flex items-center gap-1">
        <div className="w-2 h-2 rounded-full bg-green-500" />
        <span className="text-gray-500">Connected</span>
      </div>
    </div>
  );
}