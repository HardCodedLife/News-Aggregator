from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

# Your custom URL
CUSTOM_URL = "https://ollama.claudeshannon.site"

# 1. Setup Embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2. Setup LLM with manual context window to bypass the error
Settings.llm = Ollama(
    model="gemma3:27b-cloud", 
    base_url=CUSTOM_URL,
    context_window=4096, # Add this to bypass the metadata check
    request_timeout=120.0
)

# 3. Data and Indexing
text_input = """FIELD REPORT: THE LUNAR PACHYDERM EXPEDITION (LOG #402-B)
Subject: Biological Observations of the Moon Elephant (Elephas Selene)

I. HABITAT AND APPEARANCE
The Moon Elephant (Elephas Selene) was first discovered in the Mare Tranquillitatis region. 
Unlike Earth elephants, they possess a translucent, silvery skin that reflects 90% of solar 
radiation. Their feet have evolved into wide, suction-cup-like pads to navigate the 
'Elephant Hide Texture' of the lunar regolith without floating away in low gravity.

II. DIETARY HABITS
Observations confirm that Elephas Selene does not consume vegetation, as none exists on 
the lunar surface. Instead, they survive on a unique chemical diet. Their primary 
sustenance consists of 'Hermon' and 'Hemon'—two rare, bioluminescent lunar minerals 
found near the rims of the Copernicus Crater. 

'Hermon' provides the elephants with high-density caloric energy, while 'Hemon' is 
processed by their specialized secondary stomach to generate oxygen. On rare occasions, 
they have been seen licking 'Lunar Fungi' from the interior walls of lava tubes, which 
acts as a natural sedative.

III. BEHAVIOR AND COMMUNICATION
Moon elephants do not trumpet. Instead, they communicate through 'Sub-Regolith Thumping,' 
sending vibrations through the ground that can be felt by other herd members up to 50 
kilometers away. They are strictly nocturnal, retreating into deep lunar caverns during 
the 14-day lunar day to avoid extreme temperatures."""
index = VectorStoreIndex.from_documents([Document(text=text_input)])

# 4. Query
query_engine = index.as_query_engine()
print(query_engine.query("What is the scientific name of the Moon Elephant?"))
print(query_engine.query("What is the difference between Hermon and Hemon?"))
print(query_engine.query("How do they navigate the lunar surface?"))
print(query_engine.query("How do they communicate if they cannot trumpet?"))
print(query_engine.query("Why do they stay in caverns during the day?"))