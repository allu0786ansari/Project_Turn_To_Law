import { useState } from "react";
import { askQuestion } from "../api"; // Import the API function
import ResponseDisplay from "./ResponseDisplay"; // Import the ResponseDisplay component
import "../styles/QnA.css";

const QnA = ({ documentText }) => {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null); // State to store the backend response
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false); // Track API call status

  const handleAsk = async () => {
    if (loading) return; // Prevent sending another request while one is in progress
    if (!question.trim()) {
      setError("Please enter a valid question.");
      return;
    }

    setError(null); // Reset error state
    setLoading(true); // Set loading to true before request

    try {
      console.log("Sending QnA request:", { question, documentText });

      // Call the backend API
      const result = await askQuestion(question, documentText);

      if (result.response) {
        setResponse(result); // Store the response for ResponseDisplay
      } else {
        setError("No response received. Please try again.");
      }
    } catch (error) {
      console.error("Error in Q&A request:", error);
      setError("Failed to get a response. Please check your connection and try again.");
    } finally {
      setLoading(false); // Reset loading after request completes
    }
  };

  return (
    <div className="qna-container">
      <h2>Ask a Legal Question</h2>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a legal question..."
        className="qna-input"
      />
      <button
        onClick={handleAsk}
        className="qna-button"
        disabled={loading}
      >
        {loading ? <span className="spinner"></span> : "Ask"}
      </button>
      {error && <p className="qna-error">{error}</p>}

      {/* Render the ResponseDisplay component */}
      <ResponseDisplay response={response} />
    </div>
  );
};

export default QnA;
