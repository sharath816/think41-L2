const Message = ({ sender, text }: { sender: "user" | "ai"; text: string }) => {
  return (
    <div className={`my-2 p-3 rounded ${sender === "user" ? "bg-blue-100 text-right" : "bg-gray-100 text-left"}`}>
      {text}
    </div>
  );
};

export default Message;
