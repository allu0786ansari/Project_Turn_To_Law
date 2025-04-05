import { useState } from "react";
import { askQuestion } from "../api"; // Import the API function
import ResponseDisplay from "./ResponseDisplay"; // Import the ResponseDisplay component
import "../styles/QnA.css";

const QnA = ({ documentId, documentText }) => {
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

    if (!documentId || !documentText) {
      console.error("Missing documentId or documentText:", { documentId, documentText }); // Debugging log
      setError("Document is not uploaded or processed. Please upload a document first.");
      return;
    }

    setError(null); // Reset error state
    setLoading(true); // Set loading to true before request

    try {
      console.log("Sending QnA request:", { question, documentId, documentText });

      // Call the backend API
      const result = await askQuestion(question, documentId, documentText);

      if (result.answer) {
        setResponse(result); // Store the response for ResponseDisplay
      } else {
        setError("No response received. Please try again.");
      }
    } catch (error) {
      console.error("Error in Q&A request:", error);
      const errorMessage =
        error.response?.data?.detail || "Failed to get a response. Please check your connection and try again.";
      setError(errorMessage);
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
        disabled={loading} // Disable input during loading
        aria-label="Enter your legal question"
      />
      <button
        onClick={handleAsk}
        className="qna-button"
        disabled={loading || !question.trim()} // Disable button if loading or question is empty
        aria-label="Submit your question"
      >
        {loading ? <span className="spinner"></span> : "Ask"}
      </button>
      {error && <p className="qna-error">{error}</p>}

      {/* Render the ResponseDisplay component */}
      {response && <ResponseDisplay response={response} />}
    </div>
  );
};

export default QnA;
