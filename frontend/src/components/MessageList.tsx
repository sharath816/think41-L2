import { useChat } from "../context/ChatContext";
import Message from "./Message";

const MessageList = () => {
  const { messages } = useChat();
  return (
    <div>
      {messages.map((msg, index) => (
        <Message key={index} sender={msg.sender} text={msg.text} />
      ))}
    </div>
  );
};

export default MessageList;
