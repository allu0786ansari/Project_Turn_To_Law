import { useState } from "react";
import FileUpload from "../components/FileUpload"; // File upload component
import { askQuestion, factCheck } from "../api"; // API functions
import "../styles/home.css";

const Home = () => {
  const [documentText, setDocumentText] = useState(""); // Extracted text from uploaded file
  const [messages, setMessages] = useState([]); // Chat history
  const [input, setInput] = useState(""); // User input
  const [loading, setLoading] = useState(false); // Loading state
  const [error, setError] = useState(null); // Error state

  // Handle sending a question
  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]); // Add user message to chat

    setLoading(true);
    setError(null);

    try {
      const response = await askQuestion(input, documentText); // Call Q&A API
      const aiMessage = { role: "ai", content: response.response };
      setMessages((prev) => [...prev, aiMessage]); // Add AI response to chat
    } catch (err) {
      console.error("Error in Q&A:", err);
      setError("Failed to get a response. Please try again.");
    } finally {
      setLoading(false);
      setInput(""); // Clear input field
    }
  };

  // Handle fact-checking the last AI response
  const handleFactCheck = async () => {
    const lastMessage = messages[messages.length - 1];
    if (lastMessage?.role === "ai") {
      setLoading(true);
      setError(null);

      try {
        const factCheckResult = await factCheck(lastMessage.content); // Call fact-check API
        const factCheckMessage = {
          role: "fact-check",
          content: `Fact-check result: ${JSON.stringify(factCheckResult.verified_sources, null, 2)}`,
        };
        setMessages((prev) => [...prev, factCheckMessage]); // Add fact-check result to chat
      } catch (err) {
        console.error("Error in fact-checking:", err);
        setError("Failed to fact-check the response. Please try again.");
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className="home-container">
      <h1 className="home-title">Smart Legal Q&A System</h1>

      {/* File Upload Section */}
      <FileUpload
        onFileUpload={(data) => {
          setDocumentText(data.content); // Set extracted text from uploaded file
          setMessages([]); // Clear chat history when a new file is uploaded
        }}
      />

      {/* Chat Section */}
      <div className="chat-container">
        <div className="chat-history">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`chat-message ${msg.role === "user" ? "user-message" : msg.role === "ai" ? "ai-message" : "fact-check-message"}`}
            >
              {msg.content}
            </div>
          ))}
        </div>
        {error && <p className="chat-error">{error}</p>}
        <div className="chat-input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            className="chat-input"
          />
          <button onClick={handleSend} disabled={loading} className="chat-send-button">
            {loading ? "Loading..." : "Send"}
          </button>
          <button onClick={handleFactCheck} disabled={loading} className="fact-check-button">
            Validate Response
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
