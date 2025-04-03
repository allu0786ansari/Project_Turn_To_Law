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
  const formData = new FormData();
  formData.append("file_name", documentId); // ✅ Backend expects file_name, not documentId
  formData.append("question", question);

  try {
    const response = await api.post("/qna/", formData, {
      headers: {
        "Content-Type": "multipart/form-data", // ✅ Must send as FormData
      },
    });
    return response.data; // Returns { question, answer, source }
  } catch (error) {
    console.error("Q&A request failed:", error);
    throw error;
  }
};

// Fact-checking
export const factCheck = async (claim) => {
  const formData = new FormData();
  formData.append("claim", claim); // ✅ Backend expects claim, not text

  try {
    const response = await api.post("/fact-check/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data; // Returns fact-check result
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
