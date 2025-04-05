import React from "react";
import './styles/MessageList.css';
const MessageList = ({ messages }) => {
  return (
    <div className="message-list">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`message ${msg.role === "user" ? "user-message" : "assistant-message"}`}
        >
          {msg.content}
        </div>
      ))}
    </div>
  );
};

export default MessageList;