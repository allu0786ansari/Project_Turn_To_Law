const ResponseDisplay = ({ response }) => {
  if (!response) return null; // ✅ Don't render if no response

  const { answer, source, error, confidence_score } = response;

  return (
    <div className="response-container p-4 border rounded shadow bg-gray-100 mt-4">
      {error ? (
        <div className="response-error text-red-600">
          <h3 className="font-bold">Error:</h3>
          <p>{error}</p>
        </div>
      ) : (
        <div className="response-content">
          <h3 className="font-bold">Response:</h3>
          <p className="whitespace-pre-wrap">{answer || "No answer available."}</p>

          {source && (
            <div className="response-source mt-2">
              <h4 className="font-semibold">Source:</h4>
              <p className="text-sm text-gray-700">{source}</p>
            </div>
          )}

          {confidence_score !== undefined && (
            <div className="response-confidence mt-2">
              <h4 className="font-semibold">Confidence Score:</h4>
              <p className="text-sm text-gray-700">{confidence_score}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ResponseDisplay;
