import { useState } from "react";
import { askQuestion } from "../api";
import axios from 'axios';
import '../styles/QnA.css';

const QnA = ({ documentId, onResponse }) => {
  const [question, setQuestion] = useState("");

  const handleAsk = async () => {
    try {
      const response = await axios.post("/qna", { documentId, question });
      onResponse(response.data);
    } catch (error) {
      console.error("Error in Q&A", error);
    }
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
    </div>
  );
};

export default QnA;
