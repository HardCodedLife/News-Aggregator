-- 1. Enable the Vector Extension (Crucial for RAG)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create the Table
-- CREATE TABLE IF NOT EXISTS news_articles (
--     id SERIAL PRIMARY KEY,
--     title TEXT,
--     content TEXT,
--     url TEXT UNIQUE,
--     published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     embedding vector(384) -- Match all-MiniLM-L6-v2 model dimension on dev
--     -- embedding vector(3072) -- Matches your 12B model dimension
-- );
-- 
-- -- 3. Create an Index (Optional but good for speed later)
-- -- CREATE INDEX ON news_articles USING hnsw (embedding vector_cosine_ops);
