import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_threshold():
    """Return hardcoded similarity threshold"""
    return 0.65

def cosine_similarity_score(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """Calculate cosine similarity between two embeddings"""
    # Reshape embeddings to 2D arrays
    emb1 = embedding1.reshape(1, -1)
    emb2 = embedding2.reshape(1, -1)
    
    # Calculate cosine similarity
    similarity = cosine_similarity(emb1, emb2)[0][0]
    return similarity

def is_match(embedding1: np.ndarray, embedding2: np.ndarray) -> bool:
    """Check if two embeddings match based on threshold"""
    threshold = get_threshold()
    similarity = cosine_similarity_score(embedding1, embedding2)
    return similarity >= threshold

def is_match_multiple(embedding: np.ndarray, embeddings_list: list) -> bool:
    """Check if an embedding matches any in a list of embeddings"""
    threshold = get_threshold()
    for emb in embeddings_list:
        if is_match(embedding, np.array(emb)):
            return True
    return False