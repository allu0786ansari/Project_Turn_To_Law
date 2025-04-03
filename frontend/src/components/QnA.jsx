import { useState } from "react";
import axios from 'axios';
import '../styles/QnA.css';

const QnA = ({ documentId, onResponse }) => {
  const [question, setQuestion] = useState("");
  const [error, setError] = useState(null);

  const [loading, setLoading] = useState(false);  // Track API call status

const handleAsk = async () => {
    if (loading) return;  // Prevent sending another request while one is in progress
    if (!question.trim()) {
        setError("Please enter a valid question.");
        return;
    }

    setError(null);  // Reset error state
    setLoading(true); // Set loading to true before request

    try {
        console.log("Sending QnA request:", { documentId, question });

        const response = await axios.post("http://localhost:8000/qna", {  
            documentId: documentId,
            question: question,
        }, {
            headers: { "Content-Type": "application/json" }
        });

        onResponse(response.data.response);  
    } catch (error) {
        console.error("Error in Q&A request", error);
        setError("Failed to get a response. Please try again.");
    }

    setLoading(false); // Reset loading after request completes
};

  

  return (
    <div className="p-4 border rounded shadow">
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a legal question..."
        className="border p-2 w-full"
      />
      <button onClick={handleAsk} className="bg-blue-500 text-white px-4 py-2 mt-2">
        Ask
      </button>
      {error && <p className="text-red-500 mt-2">{error}</p>}
    </div>
  );
};

export default QnA;
