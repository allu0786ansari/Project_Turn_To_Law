import os
import logging
from tqdm import tqdm
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Set up environment variables
load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY is not set. Please check your .env file.")

def embed_and_save_documents():
    # Initialize embeddings and loader
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    loader = PyPDFDirectoryLoader("./Data")
    logger.info("Loader initialized")
    
    # Check if the data directory exists and is not empty
    if not os.path.exists("./Data") or not os.listdir("./Data"):
        raise FileNotFoundError("The './Data' directory is empty or does not exist.")
    
    # Load documents from the directory
    docs = loader.load()
    logger.info(f"Loaded {len(docs)} documents from './Data'")
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.split_documents(docs)
    logger.info(f"Split documents into {len(final_documents)} chunks")
    
    # Handle metadata for each document chunk
    for doc in final_documents:
        # Safely retrieve or set default metadata
        source_file = doc.metadata.get('source', "unknown")
        doc.metadata['source'] = os.path.basename(source_file)
    
    # Process documents in batches and create vector stores
    batch_size = 100
    batched_documents = [final_documents[i:i + batch_size] for i in range(0, len(final_documents), batch_size)]
    vector_stores = []
    for batch in tqdm(batched_documents, desc="Processing batches"):
        vector_store = FAISS.from_documents(batch, embeddings)
        vector_stores.append(vector_store)
    logger.info("Created vector stores for all batches")
    
    # Merge all vector stores into one
    vectors = vector_stores[0]
    for vector_store in vector_stores[1:]:
        vectors.merge_from(vector_store)
    logger.info("Merged all vector stores into a single vector database")
    
    # Save the final vector store to disk
    output_dir = "Database"
    os.makedirs(output_dir, exist_ok=True)
    vectors.save_local(output_dir)
    logger.info(f"Vector store saved to '{output_dir}'")

# Run the embedding and saving process
embed_and_save_documents()