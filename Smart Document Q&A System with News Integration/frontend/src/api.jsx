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
export const factCheck = async (aiResponse, documentId) => {
  try {
    const response = await fetch("http://localhost:8000/fact-check/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        claim: aiResponse, // The AI-generated response to validate
        document_id: documentId, // The document ID for context
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to fact-check the response.");
    }

    const data = await response.json();
    return data; // Return the fact-check results
  } catch (error) {
    console.error("Error in fact-check API call:", error);
    throw error; // Rethrow the error for the component to handle
  }
};

// ✅ Fetch Legal News
export const getNewsFeed = async (keywords = []) => {
  try {
    console.log("Fetching news with keywords:", keywords);

    const response = await api.get("/news/", {
      params: { keywords }, // Pass keywords as query parameters
    });

    if (!response.data || !response.data.news) {
      throw new Error("No news data found in the response.");
    }

    return response.data.news; // Return the news data
  } catch (error) {
    console.error("News fetch failed:", error);
    throw new Error(error.response?.data?.detail || "Failed to fetch legal news. Please try again.");
  }
};
export default api;
