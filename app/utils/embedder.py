import os
import numpy as np

# Example placeholder embedder that returns a fixed-dim zero vector or uses OpenAI
OPENAI_KEY = os.getenv("OPENAI_API_KEY", None)

def embed_text(text: str):
    """
    Return an embedding as a Python list of floats.
    Replace this function with your real embedding call (OpenAI, sentence-transformers, etc.)
    """
    # Simple deterministic placeholder (not useful for semantic search). Replace in production.
    # Choose same dimension as models.py EMBED_DIM
    dim = 1536
    # If you have OpenAI configured, you can call their embedding API here.
    # For now return zeros so DB schema is consistent.
    return [0.0] * dim
