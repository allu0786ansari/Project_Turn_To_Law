# Smart Document QA System with News Integration

A comprehensive legal document analysis system with integrated news summarization and fact-checking capabilities, designed to provide contextually relevant answers to legal queries while keeping users informed about related legal developments.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-blue.svg)
![React](https://img.shields.io/badge/react-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-blue.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Installation and Setup](#installation-and-setup)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Demo](#Demo)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview

The Smart Document QA System with News Integration is an advanced tool designed for legal professionals, researchers, and students. It combines document question-answering capabilities with legal news integration and fact-checking to provide a comprehensive legal research experience. Users can upload legal documents, ask specific questions, and receive accurate answers supplemented by relevant legal news and verified facts.

## ✨ Features

- **Document Q&A**: Upload and query legal documents to extract specific information
- **Legal News Integration**: Automatically fetch and summarize relevant legal news related to your documents or queries
- **Fact-Checking**: Verify legal claims against authoritative sources
- **Multi-Document Analysis**: Compare and contrast information across multiple legal documents
- **Contextual Understanding**: Sophisticated NLP to understand legal terminology and context
- **Citation Generation**: Proper citations for all information provided
- **Interactive UI**: User-friendly interface for document management and query processing

## 🏗️ System Architecture

The system uses a modular architecture with three primary components working together:

1. **Document Q&A Engine**: Processes uploaded documents, creates embeddings, and retrieves relevant information based on user queries
2. **News Aggregation System**: Monitors legal news sources and extracts relevant updates based on document content and user queries
3. **Fact-Checking Module**: Verifies claims by cross-referencing information with authoritative legal databases

These components are orchestrated through an agentic framework, allowing them to work collaboratively to provide comprehensive responses.

![Architecture Diagram](./docs/images/architecture.png)

## 💻 Tech Stack

### Backend
- **FastAPI**: High-performance API framework
- **LangChain**: Orchestration of AI components
- **Sentence Transformers**: Document embedding and semantic search
- **Hugging Face Transformers**: NLP models for text processing

### Frontend
- **React**: UI framework
- **CSS**: Styling
- **Axios**: API client
- **React Query**: Data fetching and caching

## 🚀 Installation and Setup

### Prerequisites
- Python 
- Node.js
- npm or yarn
- Git

### Clone the Repository
```bash
git clone https://github.com/yourusername/smart-doc-qa.git
cd smart-doc-qa
```

### Backend Setup
```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file with your API keys and configuration
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install  # or yarn install

# Create environment file
cp .env.example .env
# Edit .env file with your backend URL
```

### Starting the Application

#### Development Mode
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm start  # or yarn start
```

## 📝 Usage Guide

### 1. Document Upload
- Navigate to the upload section
- Drag and drop your legal documents (supported formats: PDF, DOCX, Image-jpg,jpeg,png)
- Wait for processing completion

### 2. Asking Questions
- Select the document(s) you want to query
- Type your legal question in the query box
- Review the answer, which includes:
  - Direct response from the document
  - Related legal news
  - Fact-check status

### 3. News Integration
- Navigate to the news tab to see all legal news related to your documents
- Filter news by relevance, date, or source

### 4. Fact-Checking
- Submit specific legal claims for verification
- Review the verification results and sources

## 🔌 API Documentation

Once the backend server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`



## 📂 Project Structure

```
smart_doc_qa/
├── backend/
│   ├── main.py               # FastAPI backend entry point
│   ├── qna.py                # Handles document Q&A
│   ├── news.py               # Legal news summarization
│   ├── fact_check.py         # Fact-checking logic
│   ├── models/               # Stores AI models or embeddings
│   ├── utils.py              # Helper functions
│   ├── config.py             # Configuration settings
│   ├── requirements.txt      # Backend dependencies
│   ├── Dockerfile            # (Optional) Containerization
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Upload.js     # File upload UI
│   │   │   ├── QueryBox.js   # User input box
│   │   │   ├── Result.js     # Displays results
│   │   ├── pages/
│   │   │   ├── Home.jsx      # Main dashboard
│   │   ├── App.js            # Main React component
│   │   ├── api.js            # Handles API calls
│   ├── package.json          # Frontend dependencies
│   ├── tailwind.config.js    # TailwindCSS for styling
│
│
├── README.md                 # Project documentation
├── .gitignore
```

## 🎬 Demo

### System Interface
![System Interface](./docs/images/interface-screenshot.png)

### Document Query Demo
![Document Query](./docs/images/query-demo.gif)

### News Integration
![News Feature](./docs/images/news-integration.png)

### Full Video Demonstration
[![Watch the video demonstration](./docs/images/video-thumbnail.png)](https://youtu.be/your-video-id)

## 🔮 Future Improvements

- **Multilingual Support**: Extend functionality to handle documents in multiple languages
- **Advanced Analytics**: Add statistical analysis of document content
- **Court Case Prediction**: Implement ML models to predict case outcomes based on document analysis
- **Collaborative Features**: Allow multiple users to work on the same documents
- **Audio Transcription**: Support for legal audio recordings and transcripts
- **Legislative Tracking**: Monitor and alert on legislative changes relevant to uploaded documents
- **Custom Training**: Allow users to fine-tune the system on their specific legal domain

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

Created by Allaudin Ansari - feel free to contact me at allu456654ansari@gmail.com
