import { Message } from "../lib/models";
import { User, Bot } from "lucide-react";

interface Props {
  message: Message;
}

export default function MessageBubble({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div className={`flex gap-3 ${isUser ? "flex-row-reverse" : ""}`}>
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${isUser ? "bg-blue-600" : "bg-gray-800"}`}>
        {isUser ? <User size={16} /> : <Bot size={16} />}
      </div>
      <div className={`max-w-[75%] rounded-xl px-4 py-2 text-sm whitespace-pre-wrap ${isUser ? "bg-blue-600 text-white" : "bg-gray-800 text-gray-100"}`}>
        {message.content}
      </div>
    </div>
  );
}