import logging
from llama_index.core import VectorStoreIndex, StorageContext, Settings, Document
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from app.core.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.index = None
        self._initialize_globals()

    def _initialize_globals(self):
        """
        Configure LlamaIndex global settings.
        This replaces the manual loading of models we did in main.py.
        """
        logger.info("⚙️ Initializing LlamaIndex Models...")

        # 1. Embedding Model (HuggingFace) - The Translator
        Settings.embed_model = HuggingFaceEmbedding(
            model_name=settings.EMBEDDING_MODEL
        )

        # 2. LLM (Ollama) - The Brain
        Settings.llm = Ollama(
            model=settings.MODEL_NAME,
            base_url=settings.OLLAMA_BASE_URL,
            request_timeout=120.0
        )

    def _get_vector_store(self):
        """Creates the Postgres connection specifically for LlamaIndex."""
        return PGVectorStore.from_params(
            database=settings.POSTGRES_DB,
            host=settings.POSTGRES_HOST,
            password=settings.POSTGRES_PASSWORD,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            table_name="news_embeddings_llama", # LlamaIndex manages this table automatically
            embed_dim=settings.EMBED_DIM
        )

    def get_index(self):
        """
        Connects to the DB and loads the Index.
        Singleton pattern: We only want to connect once.
        """
        if self.index:
            return self.index

        logger.info("🔌 Connecting to PGVector Database...")
        vector_store = self._get_vector_store()
        
        # StorageContext tells LlamaIndex "Where do I save vectors?"
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Create (or load) the index from the database
        self.index = VectorStoreIndex.from_vector_store(
            vector_store, storage_context=storage_context
        )
        return self.index

    def ingest_article(self, title: str, content: str, url: str):
        """
        The Magic Function:
        1. Takes text.
        2. Turns it into a 'Document'.
        3. Inserts it into the Index (Auto-Splitting + Auto-Embedding).
        """
        index = self.get_index()

        # Metadata is crucial for citations later
        doc = Document(
            text=content,
            metadata={
                "title": title,
                "url": url
            }
        )

        # This one line replaces 50 lines of manual splitting/embedding code!
        index.insert(doc)
        logger.info(f"✅ Indexed article: {title}")

    def query(self, question: str):
        """
        The RAG Loop:
        1. Retrieval (find relevant chunks).
        2. Synthesis (send to LLM).
        """
        index = self.get_index()

        # Create a Query Engine (The "Chat Bot" Interface)
        # streaming=False gives us a complete answer at once
        query_engine = index.as_query_engine(streaming=True)
        
        response = query_engine.query(question)
        return response

# Create a single instance to be imported elsewhere
rag_service = RAGService()
