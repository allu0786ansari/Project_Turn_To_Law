import axios from "axios";

// Base URL for the FastAPI backend
const API_BASE_URL = "http://localhost:8000"; // Change this if deployed

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// ✅ Upload Document
export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await api.post("/upload/", formData, {
      headers: {
        "Content-Type": "multipart/form-data", // Override default JSON headers
      },
    });
    return response.data; // Returns { document_id, message, content }
  } catch (error) {
    console.error("File upload failed:", error);
    throw new Error("Failed to upload the document. Please try again.");
  }
};

// ✅ Ask Question (Q&A)
export const askQuestion = async (question, documentId, documentText) => {
  // Validate input before making the API call
  if (!question || !documentId || !documentText) {
    throw new Error("Invalid input: question, documentId, and documentText are required.");
  }

  try {
    console.log("Payload sent to /qna/ endpoint:", {
      question,
      document_id: documentId,
      document_text: documentText,
    });

    const response = await api.post("/qna/", {
      question,
      document_id: documentId, // Pass the document ID
      document_text: documentText, // Pass the document content
    });
    return response.data; // Returns { question, answer, source, document_id }
  } catch (error) {
    console.error("Q&A request failed:", error);
    throw new Error("Failed to get an answer. Please try again.");
  }
};

// ✅ Fact-Checking
export const factCheck = async (claim) => {
  try {
    const response = await api.post("/fact-check/", { claim }); // Backend expects JSON
    return response.data; // Returns { claim, verified_sources, confidence_score }
  } catch (error) {
    console.error("Fact-check request failed:", error);
    throw new Error("Failed to fact-check the claim. Please try again.");
  }
};

// ✅ Fetch Legal News
export const getNewsFeed = async () => {
  try {
    const response = await api.get("/news/");
    return response.data.news; // Returns an array of news articles
  } catch (error) {
    console.error("News fetch failed:", error);
    throw new Error("Failed to fetch legal news. Please try again.");
  }
};

export default api;
