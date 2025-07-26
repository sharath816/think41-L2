import { useState } from "react";
import { useChat } from "../context/ChatContext";

const UserInput = () => {
  const [text, setText] = useState("");
  const { sendMessage, loading } = useChat();

  const handleSend = () => {
    if (text.trim()) {
      sendMessage(text);
      setText("");
    }
  };

  return (
    <div className="p-4 border-t flex">
      <input
        className="flex-1 p-2 border rounded"
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type your question..."
        disabled={loading}
      />
      <button onClick={handleSend} className="ml-2 bg-blue-500 text-white px-4 py-2 rounded" disabled={loading}>
        Send
      </button>
    </div>
  );
};

export default UserInput;
