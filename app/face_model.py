import insightface
import numpy as np
import cv2
from typing import List

# Global variable to hold the model
_model = None

def get_face_model():
    """Initialize and return the InsightFace model"""
    global _model
    if _model is None:
        _model = insightface.app.FaceAnalysis()
        _model.prepare(ctx_id=0, det_size=(640, 640))
    return _model

def extract_embeddings(image_bytes: bytes) -> List[np.ndarray]:
    """Extract face embeddings from image bytes"""
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    # Decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Get face model
    model = get_face_model()
    # Detect faces
    faces = model.get(img)
    
    # Extract embeddings
    embeddings = [face.embedding for face in faces]
    return embeddings

def extract_single_embedding(image_bytes: bytes) -> np.ndarray:
    """Extract a single face embedding from image bytes"""
    embeddings = extract_embeddings(image_bytes)
    if len(embeddings) == 0:
        raise ValueError("No face detected in the image")
    elif len(embeddings) > 1:
        raise ValueError("Multiple faces detected in the image")
    return embeddings[0]