import { useState } from "react";
import FileUpload from "../components/FileUpload";
import QnA from "../components/QnA";
import ResponseDisplay from "../components/ResponseDisplay";
import FactCheck from "../components/FactCheck";

const Home = () => {
    const [documentId, setDocumentId] = useState(null);  // Store document ID after upload
    const [response, setResponse] = useState("");  // Store the AI-generated response
    const [error, setError] = useState(null);  // Handle errors

    // Function to handle successful file upload
    const handleFileUpload = (uploadedDoc) => {
        if (uploadedDoc?.document_id) {
            setDocumentId(uploadedDoc.document_id);  // Store the document ID
            setError(null);
        } else {
            setError("File upload failed. Please try again.");
        }
    };

    return (
        <div className="p-4 max-w-2xl mx-auto">
            <h1 className="text-2xl font-bold mb-4 text-center">Legal Document Q&A</h1>

            {/* File Upload Component */}
            <FileUpload onFileUpload={handleFileUpload} />

            {error && <p className="text-red-500 mt-2">{error}</p>}

            {/* Q&A Section appears only after a document is uploaded */}
            {documentId && (
                <>
                    <QnA documentId={documentId} onResponse={setResponse} />
                    {response && <ResponseDisplay response={response} />}
                    {response && <FactCheck text={response} />}
                </>
            )}
        </div>
    );
};

export default Home;
