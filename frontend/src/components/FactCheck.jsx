import { useState } from "react";
import { factCheck } from "../api"; // Import the API function
import ResponseDisplay from "./ResponseDisplay"; // Import the ResponseDisplay component
import "../styles/FactCheck.css";

const FactCheck = () => {
  const [claim, setClaim] = useState(""); // State to store the claim
  const [response, setResponse] = useState(null); // State to store the backend response
  const [error, setError] = useState(null); // State to store errors
  const [loading, setLoading] = useState(false); // Track API call status

  const handleFactCheck = async () => {
    if (loading) return; // Prevent multiple requests
    if (!claim.trim()) {
      setError("Please provide a valid claim to fact-check.");
      return;
    }

    setError(null); // Reset error state
    setLoading(true); // Set loading to true before request

    try {
      // Call the backend API
      const result = await factCheck(claim);

      if (result.verified_sources) {
        setResponse(result); // Store the result for ResponseDisplay
      } else {
        setError("No verified sources found. Please try again.");
      }
    } catch (error) {
      console.error("Fact-check request failed:", error);
      setError("Failed to fact-check the claim. Please check your connection and try again.");
    } finally {
      setLoading(false); // Reset loading after request completes
    }
  };

  return (
    <div className="fact-check-container">
      <h2>Fact-Check a Legal Claim</h2>
      <input
        type="text"
        value={claim}
        onChange={(e) => setClaim(e.target.value)}
        placeholder="Enter a legal claim..."
        className="fact-check-input"
      />
      <button
        onClick={handleFactCheck}
        className="fact-check-button"
        disabled={loading}
      >
        {loading ? <span className="spinner"></span> : "Fact Check"}
      </button>

      {error && <p className="fact-check-error">{error}</p>}

      {/* Render the ResponseDisplay component */}
      <ResponseDisplay response={response} />
    </div>
  );
};

export default FactCheck;