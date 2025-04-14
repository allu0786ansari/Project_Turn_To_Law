# AI Powered Legal Chatbot

A Retrieval-Augmented Generation (RAG) based legal assistant chatbot that provides accurate legal information and preliminary guidance to users based on Indian legal codes, precedents, and regulations.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-blue.svg)
![React](https://img.shields.io/badge/react-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-blue.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [API Documentation](#API-Documentation)
- [Project Structure](#project-structure)
- [Legal Disclaimer](#legal-disclaimer)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)
- [Demo](#Screenshot)

## 🔍 Overview

This project implements a legal assistant chatbot specifically designed for the Indian legal system. It uses Retrieval-Augmented Generation (RAG) architecture to provide users with accurate legal information by retrieving relevant passages from a knowledge base of Indian legal documents and then generating contextually appropriate responses.

The chatbot aims to bridge the gap between complex legal information and individuals seeking preliminary legal guidance, while clearly indicating its limitations as an AI assistant.

## ✨ Features

- **Legal Information Retrieval**: Search and retrieve relevant information from Indian legal codes, precedents, and regulations
- **Context-Aware Responses**: Understand and respond to complex legal queries with contextually appropriate information
- **Legal Citation**: Properly cite legal sources when providing information
- **User-Friendly Interface**: Clean, intuitive chat interface for easy user interaction
- **Safeguards**: Built-in measures to prevent incorrect legal advice and clear disclaimer system
- **Conversation History**: Save and review previous interactions
- **Document Reference**: Direct citations to relevant legal documents
- **Responsive Design**: Works seamlessly across desktop and mobile devices

## 🏗️ Architecture

The project uses a RAG (Retrieval-Augmented Generation) architecture:

1. **Retrieval Component**: When a user submits a query, the system searches a vector database of Indian legal documents to find the most relevant passages.
2. **Generation Component**: The retrieved passages are used to augment the prompt sent to a large language model (LLM), which generates an accurate, contextual response.
3. **Validation Layer**: Responses are checked against a set of rules to ensure they meet quality standards and include proper legal disclaimers.

![Architecture Diagram](./docs/images/architecture.png)

## 💻 Tech Stack

### Backend
- FastAPI framework
- LangChain for RAG pipeline
- Vector database (FAISS)
- Large Language Model integration-Gemini
- Python

### Frontend
- React
- Vite build tool
- CSS for styling
- Axios for API requests

## 🚀 Installation and Setup

### Prerequisites
- Python
- npm or yarn
- Git

### Clone the Repository
```bash
https://github.com/allu0786ansari/Project_Turn_To_Law.git
cd AI_Powered_Legal_Chatbot
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

### Frontend Setup
```bash
cd frontend
npm install  # or yarn install
cp .env.example .env
# Edit .env file with your backend API URL
```

### Database Setup
```bash
# Make sure you have the vector database files in the Database directory
# If not, run the ingestion.py script
cd backend
python ingestion.py (store your pdf files inside data folder)
```

## 🖥️ Usage

### Running the Backend
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

### Running the Frontend
```bash
cd frontend
npm run dev  # or yarn dev/start
```

Open your browser and navigate to `http://localhost:5173` to access the chatbot interface.

## 🔌 API Documentation

Once the backend server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📂 Project Structure

```
Legal_Chatbot/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI entry point
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py          # API routes for handling chatbot queries
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── chatbot.py         # Data models for requests and responses
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── qa_service.py      # Logic for retrieval and LLM interaction
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── helpers.py         # Utility functions (e.g., metadata handling)
│   │   ├── config/
│   │   │   ├── settings.py        # Configuration for API keys and paths
│   ├── requirements.txt           # Backend dependencies
│   └── README.md                  # Backend documentation
├── frontend/
│   ├── public/                    # Static files (e.g., index.html)
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.jsx  # Main chat interface
│   │   │   ├── MessageList.jsx    # Component to display chat messages
│   │   │   ├── InputBox.jsx       # Input box for user queries
│   │   ├── api/
│   │   │   ├── apiClient.js       # Axios client for API calls
│   │   ├── App.jsx                # Main React app
│   │   ├── index.js               # React entry point
│   ├── package.json               # Frontend dependencies
│   ├── vite.config.js             # Vite configuration for React
│   └── README.md                  # Frontend documentation
├── Database/                      # Vector database files (e.g., index, index.pkl)
├── .env                           # Environment variables for API keys
├── .gitignore                     # Git ignore file
└── README.md                      # Project overview
```

## ⚠️ Legal Disclaimer

This chatbot is designed to provide preliminary legal information based on Indian legal codes(Constitution of India, criminal law 2018, IPC 1860, criminal procedure 1973, it code...etc), precedents, and regulations. However:

- The information provided by this chatbot does not constitute legal advice.
- This chatbot is not a substitute for consultation with a qualified legal professional.
- Users should verify any information provided before acting on it.
- The developers are not responsible for any actions taken based on the information provided by this chatbot.

## 🔮 Future Improvements

- [ ] Advanced entity recognition for legal terms
- [ ] Integration with legal document generators
- [ ] Case-specific personalization based on user history
- [ ] Enhanced multilingual support for more Indian languages
- [ ] Machine learning model for legal outcome prediction
- [ ] Integration with court schedule APIs
- [ ] Voice interface for accessibility

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Created by Allaudin Ansari - feel free to contact me at allu456654ansari@gmail.com!

## Demo
![Chatbot Interface](https://github.com/allu0786ansari/Project_Turn_To_Law/blob/main/AI_Powered_Legal_Chatbot/backend/Demo_Legal_Chatbot.png)


### Demo Video

https://github.com/yourusername/your-repo/assets/your-asset-id/demo-video.mp4
