# 📰 AI-Powered News Aggregator (RAG)
A local Retrieval-Augmented Generation (RAG) platform that allows users to ingest news articles and chat with an AI to gain insights based **strictly** on the ingested content.

## 🏗 Tech Stack
* **Frontend:** React + Typescript (Vite)
* ** Backend:** Python (FastAPI + LangChain)
* **Database:** PostgreSQL (pgvector)
* **AI Engine:** Ollama (Local LLM) + HuggingFace (Embeddings)
* **Infrastructure:** Docker Compose

--

## 🚀 Quick Start

### 1. Prerequisites
- Docker Desktop (Running)
- Git

### 2. Installation
```bash
# 1. Clone the repository
git clone https://github.com/HardCodedLife/News-Aggregator.git
cd News-Aggregator

# 2. Start the application
docker-compose up -d --build
```

-----

## ⚙️ First Run Setup (Crucial\!)

After the containers are running, you must perform these *one-time manual steps* to initialize the AI models.

### 1. Pull the LLM (Ollama)

The chat model is not downloaded by default. Run this command to pull it into the container:
```bash
# Pull the specific model used in backend/main.py
docker-compose exec ollama sh # Access the backend container
$ ollama pull gemini-3-pro-preview
$ exit # Exit the container

# (Optional) Pull a backup lightweight model if the above fails
docker-compose exec ollama ollama pull llama3.2
```

### 2. Verify Database Schema (If changing models)

The project is currently configured for small development embedding models (**384 dimensions**).

* **Current Model:** `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
* **Required DB Column:** `vector(384)`

If you ever switch to a larger model (e.g., tencent/KaLM-Embedding-Gemma3-12B-2511)

1. Update `db_scripts/init.sql` to `vector(3072)`.
2. Update `backend/main.py` to load the larger model.
3. **Wipe the database** to apply changes (see Troubleshooting).

-----

## 🔮 Future Roadmap

This project is currently in the **Prototype Phase** (Phase 1). The following upgrades are planned for Phase 2:

### 1\. Migration to LlamaIndex

  * **Goal:** Replace the manual RAG logic in `main.py` with **LlamaIndex**.
  * **Why:** LlamaIndex offers superior data ingestion strategies (hierarchical indexing) and better retrieval performance (re-ranking) compared to manual vector search.
  * **Implementation:**
      * Use `VectorStoreIndex` to manage the Postgres connection.
      * Implement a `QueryEngine` for the chat interface.

### 2\. Advanced Embedding Management

  * **Goal:** Support high-performance, large-scale embedding models.
  * **Target Model:** `tencent/KaLM-Embedding-Gemma3-12B-2511` (SOTA).
  * **Strategy:**
      * Integrate LlamaIndex's `HuggingFaceEmbedding` class to manage model loading efficiently.
      * Implement caching mechanisms to prevent reloading 12GB+ models on container restarts.

### 3\. Automated Data Pipeline

  * **Goal:** Remove manual `/ingest` calls.
  * **Feature:** Build a background worker (using Celery or a simple Cron loop) that automatically fetches top headlines from NewsAPI/RSS feeds every hour and processes them into the vector database.

-----

## 🖥️ Usage Guide

### Access Points

| Service | URL | Description |
| :--- | :--- | :--- |
| **Frontend UI** | [http://localhost:3000](https://www.google.com/search?q=http://localhost:3000) | The main interface for users. |
| **Backend API** | [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs) | Swagger UI for testing API endpoints. |
| **Health Check** | [http://localhost:8000/health](https://www.google.com/search?q=http://localhost:8000/health) | Verify DB and AI connections. |

### How to use the App

1.  **Ingest News:**
      * Go to the Frontend.
      * Enter a Title, URL, and paste the Article Content.
      * Click **Ingest**. (This splits the text into chunks, calculates vectors, and saves to Postgres).
2.  **Chat:**
      * Ask a question related to the news you just added.
      * The AI will search the database and answer using *only* that information.

-----

## 🛠 Troubleshooting

### "Dimension mismatch" Error (384 vs 3072)

If you see an error saying `expected 3072 dimensions, not 384` (or vice versa), your Database schema does not match your Python embedding model.

**The Fix (Wipe & Reset):**

```bash
# 1. Stop containers and DELETE the database volume
docker-compose down -v

# 2. Restart (The init.sql script will run again with correct settings)
docker-compose up -d
```

### "Container name already in use"

If Docker complains about a conflict with `ollama` or another container:

```bash
# Force delete the zombie container
docker rm -f ollama

# Or clean up everything
docker-compose down --remove-orphans
```

### Frontend says "Vite requires Node.js version..."

Your `node_modules` might be stale or built with an old Node version.

```bash
# 1. Delete local node_modules
rm -rf frontend/node_modules

# 2. Rebuild the container
docker-compose up -d --build frontend
```

-----

## 🗑 Uninstalling / Cleanup

If you want to completely remove the project, including all data, models, and Docker images, follow these steps.

**⚠️ WARNING:** This will delete your database and all downloaded AI models (saving you \~20GB of disk space).

```bash
# 1. Stop containers and remove volumes (Deletes DB & Models)
docker-compose down -v

# 2. Remove the Docker images created by this project
docker rmi news_backend news_frontend

# 3. (Optional) Remove orphaned containers
docker system prune -f
```

-----

## 📂 Project Structure

```text
news-aggregator/
├── docker-compose.yml       # Orchestration
├── db_scripts/
│   └── init.sql             # SQL to create 'news_articles' table
├── backend/
│   ├── Dockerfile           # Python 3.11 environment
│   ├── main.py              # FastAPI + RAG Logic
│   └── requirements.txt     # Python dependencies
└── frontend/
    ├── Dockerfile           # Node.js environment
    ├── package.json         # React dependencies
    └── src/                 # React Source Code
```
 
