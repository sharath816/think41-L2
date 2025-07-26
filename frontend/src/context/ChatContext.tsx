import { createContext, useContext, useState, useEffect } from "react";

type Message = { sender: "user" | "ai"; text: string };
type ChatContextType = {
    messages: Message[];
    loading: boolean;
    sendMessage: (msg: string) => void;
    selectedSession: string;
    setSelectedSession: (id: string) => void;
    sessions: string[];
};

const ChatContext = createContext<ChatContextType>({} as ChatContextType);

export const ChatProvider = ({ children }: { children: React.ReactNode }) => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [loading, setLoading] = useState(false);
    const [sessions, setSessions] = useState<string[]>(["session1", "session2"]);
    const [selectedSession, setSelectedSession] = useState("session1");

    const sendMessage = async (msg: string) => {
        const userMsg: Message = { sender: "user", text: msg };
        setMessages((prev) => [...prev, userMsg]);
        setLoading(true);

        try {
            const res = await fetch("http://localhost:8000/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    user_id: "sharath123", // Hardcoded or use auth ID
                    message: msg,
                    conversation_id: selectedSession // map to Mongo ObjectId string
                }),
            });

            const data = await res.json();
            const aiMsg: Message = { sender: "ai", text: data.response };
            setMessages((prev) => [...prev, aiMsg]);
        } catch (error) {
            console.error("Error sending message:", error);
            const aiMsg: Message = {
                sender: "ai",
                text: "Sorry, something went wrong.",
            };
            setMessages((prev) => [...prev, aiMsg]);
        } finally {
            setLoading(false);
        }
    };


    // Load session data on change
    useEffect(() => {
        // Fetch messages for selectedSession from backend
        async function fetchHistory() {
            const res = await fetch(`http://localhost:8000/api/history/${selectedSession}`);
            const data = await res.json();
            setMessages(data.messages);
        }
        fetchHistory();
    }, [selectedSession]);

    return (
        <ChatContext.Provider value={{ messages, loading, sendMessage, selectedSession, setSelectedSession, sessions }}>
            {children}
        </ChatContext.Provider>
    );
};

export const useChat = () => useContext(ChatContext);
