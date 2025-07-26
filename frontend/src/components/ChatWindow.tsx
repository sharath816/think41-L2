import MessageList from "./MessageList";
import UserInput from "./UserInput";
import { useChat } from "../context/ChatContext";

const ChatWindow = () => {
  const { sessions, selectedSession, setSelectedSession } = useChat();

  return (
    <div className="flex h-screen">
      {/* Sidebar for session history */}
      <div className="w-1/4 p-4 border-r">
        <h3 className="text-lg font-semibold mb-2">Conversations</h3>
        {sessions.map((s) => (
          <div
            key={s}
            className={`p-2 cursor-pointer rounded ${selectedSession === s ? "bg-blue-200" : "hover:bg-gray-100"}`}
            onClick={() => setSelectedSession(s)}
          >
            {s}
          </div>
        ))}
      </div>

      {/* Chat area */}
      <div className="flex flex-col flex-1">
        <div className="flex-1 overflow-y-auto p-4">
          <MessageList />
        </div>
        <UserInput />
      </div>
    </div>
  );
};

export default ChatWindow;
