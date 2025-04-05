import { useState } from "react";
import "../styles/FileUpload.css";

const FileUpload = ({ onFileUpload }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");

  // Show success or error messages
  const showMessage = (msg, type) => {
    setMessage(msg);
    setMessageType(type);
  };

  // Handle file selection
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const allowedTypes = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
        "image/png",
        "image/jpeg",
        "image/jpg",
      ];
      if (!allowedTypes.includes(selectedFile.type)) {
        showMessage("Invalid file type. Please upload a PDF, DOCX, or image file.", "error");
        setFile(null);
        return;
      }
      setFile(selectedFile);
      setMessage("");
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      showMessage("Please select a file to upload.", "error");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log("Backend response:", data);

      if (response.ok) {
        if (data.document_id) {
          showMessage(`Success! Document ID: ${data.document_id}`, "success");
          onFileUpload(data); // Pass document details (including document_id) to parent component
        } else {
          showMessage("Success! But document ID is missing.", "warning");
        }
      } else {
        showMessage(`Error: ${data.detail || "Something went wrong"}`, "error");
      }
    } catch (error) {
      console.error("File upload failed:", error);
      showMessage(`Error: ${error.message || "Network error"}`, "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Your Document</h2>
      <p>Upload a PDF, DOCX, or image file to analyze</p>

      <form onSubmit={handleSubmit}>
        <div className="file-input">
          <input
            type="file"
            accept=".pdf,.doc,.docx,.png,.jpg,.jpeg"
            id="file-upload"
            onChange={handleFileChange}
            disabled={loading} // Disable input during loading
            aria-label="Choose a file to upload"
          />
          <label htmlFor="file-upload" className="custom-file-upload">
            Choose File
          </label>
          <span className="file-name">{file ? file.name : "No file selected"}</span>
        </div>

        <button type="submit" className="submit-btn" disabled={!file || loading}>
          {loading ? <span className="spinner"></span> : "Upload Document"}
        </button>

        {message && (
          <div className={`message ${messageType}`} aria-live="polite">
            {message}
          </div>
        )}
      </form>
    </div>
  );
};

export default FileUpload;