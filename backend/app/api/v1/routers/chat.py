from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.schemas import ChatRequest
from app.services.index_service import rag_service
import json

router = APIRouter()

@router.post("/chat") 
def chat(request: ChatRequest):
    try:
        # 1. Ask LlamaIndex
        streaming_response = rag_service.query(request.question)
        
        # 2. Extract Sources (Evidence)
        # LlamaIndex returns 'source_nodes' which contain the chunks used

        def event_generator():
            #Iterate through the stream as it arrives
            for token in streaming_response.response_gen:
                # We yield raw text (could be JSON if needed)
                yield token

                    
        return StreamingResponse(event_generator(), media_type="text/plain") 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
