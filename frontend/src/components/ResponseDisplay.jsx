const ResponseDisplay = ({ response }) => {
    return (
      <div className="p-4 border rounded shadow bg-gray-100 mt-4">
        <h3 className="font-bold">Response:</h3>
        <p>{response}</p>
      </div>
    );
  };
  
  export default ResponseDisplay;
  