import React, { useState } from "react";
import MessageList from "./MessageList";
import InputBox from "./InputBox";
import { queryChatbot } from "../api/apiClient";
import './styles/ChatInterface.css';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);

  const handleSend = async (message) => {
    const userMessage = { role: "user", content: message };
    setMessages((prev) => [...prev, userMessage]);

    const assistantMessage = { role: "assistant", content: "Thinking..." };
    setMessages((prev) => [...prev, assistantMessage]);

    try {
      const response = await queryChatbot(message);
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = { role: "assistant", content: response };
        return updated;
      });
    } catch (error) {
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = { role: "assistant", content: "Error: Unable to fetch response." };
        return updated;
      });
    }
  };

  return (
    <div className="chat-interface">
      <MessageList messages={messages} />
      <InputBox onSend={handleSend} />
    </div>
  );
};

export default ChatInterface;