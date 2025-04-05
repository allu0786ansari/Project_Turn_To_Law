import os
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load a transformer model optimized for legal text
MODEL_NAME = os.getenv("EMBEDDING_MODEL", "sentence-transformers/msmarco-distilbert-base-v4")
model = SentenceTransformer(MODEL_NAME)

def generate_embedding(text: str) -> np.ndarray:
    """
    Generate a dense vector embedding for a given text input.
    :param text: The input legal document text or query.
    :return: A NumPy array representing the embedding.
    """
    return model.encode(text, convert_to_numpy=True)

def batch_generate_embeddings(texts: list) -> np.ndarray:
    """
    Generate embeddings for a batch of text inputs.
    :param texts: A list of legal documents or queries.
    :return: A NumPy array of embeddings.
    """
    return model.encode(texts, convert_to_numpy=True)
