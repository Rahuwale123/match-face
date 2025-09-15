from fastapi import APIRouter, UploadFile, File, HTTPException
import json
import numpy as np
from ..db import get_db_connection
from ..face_model import extract_single_embedding
from ..utils.similarity import is_match_multiple
from ..utils.validators import validate_image_file

router = APIRouter()

@router.post("/match_face")
async def match_face(file: UploadFile = File(..., description="Face image for matching")):
    """
    Match a face image against stored embeddings and return access status
    """
    try:
        # Read file content
        contents = await file.read()
        
        # Validate file
        if not validate_image_file(contents):
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Extract embedding from uploaded image
        query_embedding = extract_single_embedding(contents)
        
        # Fetch all embeddings from database
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT user_id, name, embedding FROM faces")
        rows = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        # Convert rows to list of embeddings
        embeddings_list = []
        user_ids = []
        names = []
        
        for row in rows:
            user_id, name, embedding_json = row
            embedding = np.array(json.loads(embedding_json))
            embeddings_list.append(embedding)
            user_ids.append(user_id)
            names.append(name)
        
        # Check for matches
        for i, embedding in enumerate(embeddings_list):
            if is_match_multiple(query_embedding, [embedding]):
                return {
                    "status": "access_granted",
                    "user_id": user_ids[i],
                    "name": names[i]
                }
        
        # No match found
        return {
            "status": "access_denied"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))