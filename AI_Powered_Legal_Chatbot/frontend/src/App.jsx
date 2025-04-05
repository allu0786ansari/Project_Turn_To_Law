import React from "react";
import ChatInterface from "./components/ChatInterface";
import "./App.css"; // Optional: Add styles for the chatbot

const App = () => {
  return (
    <div className="app">
      <h1>Legal Chatbot</h1>
      <ChatInterface />
    </div>
  );
};

export default App;
