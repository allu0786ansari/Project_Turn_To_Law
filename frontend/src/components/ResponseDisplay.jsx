const ResponseDisplay = ({ response }) => {
  if (!response) return null; // ✅ Don't render if no response

  return (
    <div className="p-4 border rounded shadow bg-gray-100 mt-4">
      <h3 className="font-bold">Response:</h3>
      <p className="whitespace-pre-wrap">{response}</p> {/* ✅ Preserve formatting */}
    </div>
  );
};

export default ResponseDisplay;
