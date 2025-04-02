import axios from "axios";

// Base URL for the FastAPI backend
const API_BASE_URL = "http://localhost:8000"; // Change this if deployed

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Upload document
export const uploadDocument = async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    
    try {
      const response = await api.post("/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data", // Override default JSON headers
        },
      });
      return response.data; // Returns document ID
    } catch (error) {
      console.error("File upload failed:", error);
      throw error;
    }
  };
  

// Ask question
export const askQuestion = async (documentId, question) => {
  try {
    const response = await api.post("/qna", { documentId, question });
    return response.data; // Returns generated response
  } catch (error) {
    console.error("Q&A request failed:", error);
    throw error;
  }
};

// Fact-checking
export const factCheck = async (text) => {
  try {
    const response = await api.post("/fact-check", { text });
    return response.data.result; // Returns fact-check result
  } catch (error) {
    console.error("Fact-check request failed:", error);
    throw error;
  }
};

// Fetch legal news
export const getNewsFeed = async () => {
  try {
    const response = await api.get("/news");
    return response.data; // Returns news articles
  } catch (error) {
    console.error("News fetch failed:", error);
    throw error;
  }
};

export default api;
