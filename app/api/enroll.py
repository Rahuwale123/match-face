from fastapi import APIRouter, UploadFile, File, Path, HTTPException, Form
from typing import List
import json
import numpy as np
from ..db import get_db_connection
from ..face_model import extract_embeddings
from ..utils.validators import validate_image_file

router = APIRouter()

@router.post("/enroll_faces/{user_id}")
async def enroll_faces(
    user_id: str = Path(..., description="User ID for face enrollment"),
    name: str = Form(..., description="User name for face enrollment"),
    files: List[UploadFile] = File(..., description="Multiple face images for enrollment (maximum 4 images)", max_items=4)
):
    """
    Enroll multiple face images for a user and store their embeddings
    """
    try:
        # Validate input
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        # Check if more than 4 files are provided
        if len(files) > 4:
            raise HTTPException(status_code=400, detail="Maximum 4 images allowed per enrollment")
        
        # Extract embeddings from all images
        all_embeddings = []
        for file in files:
            # Read file content
            contents = await file.read()
            
            # Validate file
            if not validate_image_file(contents):
                raise HTTPException(status_code=400, detail=f"Invalid image file: {file.filename}")
            
            # Extract embeddings
            embeddings = extract_embeddings(contents)
            
            # Add embeddings to list
            all_embeddings.extend(embeddings)
        
        # Store embeddings in database
        connection = get_db_connection()
        cursor = connection.cursor()
        
        faces_stored = 0
        for embedding in all_embeddings:
            # Convert embedding to JSON string for storage
            embedding_json = json.dumps(embedding.tolist())
            
            # Insert into database
            cursor.execute(
                "INSERT INTO faces (user_id, name, embedding) VALUES (%s, %s, %s)",
                (user_id, name, embedding_json)
            )
            faces_stored += 1
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return {
            "status": "success",
            "faces_stored": faces_stored
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))