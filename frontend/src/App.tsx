import { useState } from "react";
import { useSession } from "./hooks/useSession";
import ChatWindow from "./components/ChatWindow";

export default function App() {
  return <ChatWindow />;
}