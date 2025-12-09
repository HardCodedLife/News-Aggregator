import os
import requests
import psycopg2
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --------------------------------------------------------------------------
# 1. GLOBAL STATE
# --------------------------------------------------------------------------
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 STARTUP: Loading Embedding Model...")
    try:
        # Smallest, fastest model for development (80MB)
        ml_models["embeddings"] = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2", 
            model_kwargs={'device': 'cpu'}
        )
        print("✅ Model Loaded Successfully!")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
    yield
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

# --------------------------------------------------------------------------
# 2. CONFIG
# --------------------------------------------------------------------------
origins = ["http://localhost:3000", "http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------------------------
# 3. DATABASE CONNECTION
# --------------------------------------------------------------------------
def get_db_connection():
    return psycopg2.connect(
        host="db",
        database="vectordb",
        user="user",
        password="password"
    )

# --------------------------------------------------------------------------
# 4. DATA MODELS
# --------------------------------------------------------------------------
class NewsItem(BaseModel):
    title: str
    content: str
    url: str

class ChatRequest(BaseModel):
    question: str

# --------------------------------------------------------------------------
# 5. ENDPOINTS
# --------------------------------------------------------------------------

@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": "embeddings" in ml_models}

@app.post("/ingest")
def ingest_news(item: NewsItem):
    """
    1. Splits text into chunks (The 'Split' you missed).
    2. Embeds each chunk.
    3. Saves all chunks to DB.
    """
    if "embeddings" not in ml_models:
        raise HTTPException(status_code=503, detail="Model not loaded yet")

    try:
        # STEP A: CHUNKING (The Missing Part)
        # We split long articles into pieces of 500 characters with some overlap.
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(item.content)

        print(f"✂️ Split article into {len(chunks)} chunks.")

        conn = get_db_connection()
        cur = conn.cursor()

        # STEP B: EMBED & SAVE LOOP
        saved_count = 0
        for chunk_text in chunks:
            # Create vector for this specific chunk
            vector = ml_models["embeddings"].embed_query(chunk_text)
            
            # Save chunk to DB
            # We save the *Same* Title/URL for all chunks, but different content
            cur.execute(
                "INSERT INTO news_articles (title, content, url, embedding) VALUES (%s, %s, %s, %s)",
                (item.title, chunk_text, item.url, vector)
            )
            saved_count += 1
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {"status": "success", "chunks_saved": saved_count}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat_rag(request: ChatRequest):
    if "embeddings" not in ml_models:
        raise HTTPException(status_code=503, detail="Model not loaded yet")

    try:
        # 1. Embed Question
        question_vector = ml_models["embeddings"].embed_query(request.question)
        
        # 2. Search DB (Find top 3 most relevant CHUNKS)
        conn = get_db_connection()
        cur = conn.cursor()
        search_query = """
        SELECT title, content, url, 1 - (embedding <=> %s::vector) as similarity
        FROM news_articles
        ORDER BY embedding <=> %s::vector
        LIMIT 3;
        """
        cur.execute(search_query, (question_vector, question_vector))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        if not rows:
            return {"answer": "No relevant news found.", "sources": []}
            
        # 3. Build Context
        context_text = "\n\n".join([f"Source: {r[0]}\nSnippet: {r[1]}" for r in rows])
        
        # 4. Call Ollama
        prompt = f"""Use the following news snippets to answer the question.
        
        News Snippets:
        {context_text}
        
        Question: {request.question}
        """
        
        # CORRECTED URL VARIABLE
        ollama_url = os.getenv("OLLAMA_API_URL", "http://ollama:11434")
        
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": "gemini-3-pro-preview:latest", # CORRECTED MODEL NAME
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code != 200:
             return {"error": f"Ollama Error: {response.text}"}

        llm_response = response.json().get("response", "Error generating response")
        
        return {
            "answer": llm_response,
            "sources": [{"title": r[0], "url": r[2]} for r in rows]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
