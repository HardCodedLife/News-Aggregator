from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# NOTE: We now import from the 'v1' folder
from app.api.v1.routers import ingest, chat
from app.core.config import settings

# 1. Initialize the Application
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 2. CORS Configuration 
# (Allows your React Frontend on port 3000 to talk to this Backend)
origins = ["http://localhost:3000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Register Routers
# We prefix everything with /api/v1 so the URL is http://localhost:8000/api/v1/chat
app.include_router(ingest.router, prefix=settings.API_V1_STR, tags=["Ingestion"])
app.include_router(chat.router, prefix=settings.API_V1_STR, tags=["Chat"])

# 4. Global Health Check
@app.get("/health", tags=["Status"])
def health_check():
    """
    A simple ping to verify the server is running.
    """
    return {
        "status": "ok", 
        "system": "LlamaIndex RAG Production", 
        "version": "v1"
    }
