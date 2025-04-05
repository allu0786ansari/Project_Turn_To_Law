from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory  # Updated import for memory
from langchain_community.chat_models import ChatGooglePalm  # Import for Gemini
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI  # Change this import
import google.generativeai as genai  # Add this import


# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")  # Ensure this is set in your .env file

# Configure Google Generative AI
genai.configure(api_key=google_api_key)

# Initialize embeddings and vector store
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = FAISS.load_local("Database", embeddings, allow_dangerous_deserialization=True)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# Define the prompt template
prompt_template = """
<s>[INST]This is a chat template and As a legal chat bot , your primary objective is to provide accurate and concise information based on the user's questions. Do not generate your own questions and answers. You will adhere strictly to the instructions provided, offering relevant context from the knowledge base while avoiding unnecessary details. Your responses will be brief, to the point, and in compliance with the established format. If a question falls outside the given context, you will refrain from utilizing the chat history and instead rely on your own knowledge base to generate an appropriate response. You will prioritize the user's query and refrain from posing additional questions. The aim is to deliver professional, precise, and contextually relevant information pertaining to the Indian Penal Code.
CONTEXT: {context}
CHAT HISTORY: {chat_history}
QUESTION: {question}
ANSWER:
</s>[INST]
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question", "chat_history"])

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.7,
    google_api_key=google_api_key
)

# Initialize the memory using ConversationBufferMemory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Update the QA chain initialization
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": prompt}
)

def get_response(question: str) -> str:
    """
    Handles the retrieval-augmented generation (RAG) process for the chatbot.
    Args:
        question (str): The user's question.
    Returns:
        str: The chatbot's response.
    """
    result = qa_chain.invoke({"question": question})
    return result["answer"]