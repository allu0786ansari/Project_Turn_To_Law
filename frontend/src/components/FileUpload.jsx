import { useState } from "react";
import "../styles/FileUpload.css";

const FileUpload = ({ onFileUpload }) => {  // Accept prop to pass documentId
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState("");

    const showMessage = (msg, type) => {
        setMessage(msg);
        setMessageType(type);
    };

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            const allowedTypes = ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];
            if (!allowedTypes.includes(selectedFile.type)) {
                showMessage("Invalid file type. Please upload a PDF or DOC file.", "error");
                setFile(null);
                return;
            }
            setFile(selectedFile);
            setMessage("");
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            showMessage("Please upload a file", "error");
            return;
        }

        const formData = new FormData();
        formData.append("file_type", "document");
        formData.append("file", file);

        setLoading(true);

        try {
            const response = await fetch("http://localhost:8000/upload/", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();
            console.log("Response Data:", data); // Debugging

            if (response.ok) {
                if (data.document_id) {
                    showMessage(`Success! Document ID: ${data.document_id}`, "success");
                    console.log("Document ID:", data.document_id);
                    
                    // 🔹 Pass documentId to the parent component
                    onFileUpload(data);
                } else {
                    showMessage("Success! But document ID is missing.", "warning");
                }
            } else {
                showMessage(`Error: ${data.detail || "Something went wrong"}`, "error");
            }
        } catch (error) {
            showMessage(`Error: ${error.message || "Network error"}`, "error");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="upload-container">
            <h2>Upload Your Document</h2>
            <p>Upload a PDF or DOC file to analyze</p>

            <form onSubmit={handleSubmit}>
                <div className="file-input">
                    <input type="file" accept=".pdf,.doc,.docx" id="file-upload" onChange={handleFileChange} />
                    <label htmlFor="file-upload" className="custom-file-upload">
                        Choose File
                    </label>
                    <span className="file-name">{file ? file.name : ""}</span>
                </div>

                <button type="submit" className="submit-btn" disabled={!file || loading}>
                    {loading ? <span className="spinner"></span> : "Upload Document"}
                </button>

                {message && <div className={`message ${messageType}`}>{message}</div>}
            </form>
        </div>
    );
};

export default FileUpload;
