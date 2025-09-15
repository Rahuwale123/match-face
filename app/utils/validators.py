import numpy as np

def validate_image_file(file_content: bytes) -> bool:
    """Validate if the file content is a valid image"""
    # Basic validation - check if file has content
    if not file_content:
        return False
    return True

def validate_embedding(embedding: np.ndarray) -> bool:
    """Validate if the embedding is valid"""
    # Check if embedding is a numpy array
    if not isinstance(embedding, np.ndarray):
        return False
    
    # Check if embedding has data
    if embedding.size == 0:
        return False
    
    return True