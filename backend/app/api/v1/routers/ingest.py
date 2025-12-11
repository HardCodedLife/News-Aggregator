from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.schemas import NewsIngest
from app.services.index_service import rag_service

router = APIRouter()

def process_ingestion(title: str, content: str, url: str):
    """Wrapper to run the heavy lifting"""
    try:
        # This blocks the thread, but not the main loop
        rag_service.ingest_article(title, content, url)
        print(f"✅ Background Task Finished: {title}")
    except Exception as e:
        print(f"❌ Background Task Failed: {e}")

@router.post("/ingest")
async def ingest_news(item: NewsIngest, background_tasks: BackgroundTasks):
    """
    Accepts the article and processes it in the background.
    Returns immediately so the UI doesn't freeze.
    """
    # Add the function to the queue
    background_tasks.add_task(process_ingestion, item.title, item.content, item.url)
    
    return {
        "status": "accepted", 
        "message": "Ingestion started in background. You can chat about it shortly."
    }
