# Face Recognition API

A real-time face recognition system built with FastAPI, InsightFace, and MySQL.

## Features

- **Face Enrollment API**: Accept multiple face images per user and store embeddings only (maximum 4 images)
- **Face Match API**: Match a user-uploaded face against stored embeddings in milliseconds
- **Privacy-focused**: Stores only embeddings, not actual images
- **Scalable**: Designed for future integration with vector search engines like FAISS/Milvus

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MySQL
- **Face Embeddings**: InsightFace
- **Vector Search** (Optional): FAISS / Milvus

## API Endpoints

### 1. Enroll Faces

**URL**: `/enroll_faces/{user_id}`

**Method**: `POST`

**Input**: 
- Path parameter: `user_id` (User ID for face enrollment)
- Form parameter: `name` (User name for face enrollment)
- Files: Multiple face images (multipart/form-data, maximum 4 images)

**Output**: 
```json
{
  "status": "success",
  "faces_stored": 3
}
```

### 2. Match Face

**URL**: `/match_face`

**Method**: `POST`

**Input**: Single face image (multipart/form-data)

**Output**: 
```json
// if matched
{
  "status": "access_granted",
  "user_id": "user123",
  "name": "John Doe"
}

// if not matched
{
  "status": "access_denied"
}
```

## Database Schema

Table: `faces`

| Column | Type | Notes |
|--------|------|-------|
| id | INT PK AI | Auto-increment |
| user_id | VARCHAR | Provided at enrollment |
| name | VARCHAR | User name |
| embedding | TEXT/BLOB | Face embedding vector |
| created_at | TIMESTAMP | Auto now |

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Update database configuration in `app/db.py` with your MySQL credentials

3. Run the application:
   ```bash
   python run.py
   ```

## Performance & Scaling

- Current Setup: Linear scan over embeddings → works for thousands of faces in <100ms
- Future Optimization: Use FAISS / Milvus for billion-scale embeddings
- No images stored: Reduces DB size, simplifies privacy concerns
- Threshold tuning: Cosine similarity threshold (0.6–0.7) to avoid false positives