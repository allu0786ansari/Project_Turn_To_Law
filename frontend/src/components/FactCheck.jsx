import { useState } from "react";
import { factCheck } from "../api"; // Import the API function
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
      console.log("Sending fact-check request for claim:", claim);

      // Call the backend API
      const result = await factCheck(claim);

      if (result && result.results) {
        setResponse(result); // Store the result for display
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
        disabled={loading} // Disable input during loading
        aria-label="Enter a legal claim to fact-check"
      />
      <button
        onClick={handleFactCheck}
        className="fact-check-button"
        disabled={loading || !claim.trim()} // Disable button if loading or claim is empty
        aria-label="Submit your claim for fact-checking"
      >
        {loading ? <span className="spinner"></span> : "Fact Check"}
      </button>

      {error && <p className="fact-check-error">{error}</p>}

      {/* Render the fact-check results */}
      {response && (
        <div className="fact-check-results">
          <h3>Fact-Check Results</h3>
          <p><strong>Claim:</strong> {response.claim}</p>
          <p><strong>Summary:</strong></p>
          <ul>
            <li>Supports: {response.summary.supports}</li>
            <li>Contradicts: {response.summary.contradicts}</li>
            <li>Irrelevant: {response.summary.irrelevant}</li>
            <li>Errors: {response.summary.errors}</li>
          </ul>
          <h4>Detailed Results:</h4>
          <ul>
            {response.results.map((result, index) => (
              <li key={index}>
                <p><strong>Status:</strong> {result.status}</p>
                <p><strong>Reasoning:</strong> {result.reasoning}</p>
                <p><strong>Quote:</strong> {result.quote || "N/A"}</p>
                <p>
                  <strong>Source URL:</strong>{" "}
                  <a href={result.source_url} target="_blank" rel="noopener noreferrer">
                    {result.source_url}
                  </a>
                </p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FactCheck;