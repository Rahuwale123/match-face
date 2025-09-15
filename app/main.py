from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.enroll import router as enroll_router
from .api.match import router as match_router
from .db import init_db
import uvicorn
import sys

app = FastAPI(
    title="Face Recognition API",
    description="A real-time face recognition system with enrollment and matching capabilities",
    version="1.0.0"
)

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(enroll_router)
app.include_router(match_router)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        print("Please check your MySQL server and credentials in app/db.py")
        # We won't exit here to allow the API to start even if DB init fails
        # In a production environment, you might want to handle this differently

@app.get("/")
async def root():
    return {"message": "Face Recognition API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)