import axios from "axios";

const apiClient = axios.create({
    baseURL: "http://127.0.0.1:8000/api",
    headers: {
        'Content-Type': 'application/json',
    },
});

export const queryChatbot = async (question) => {
    try {
        const response = await apiClient.post("/query", { question });
        return response.data.answer;
    } catch (error) {
        console.error("API Error:", error);
        throw new Error(error.response?.data?.message || "Failed to get response from chatbot");
    }
};