# Advanced Configuration for SEN RAG Assistant
# This file contains tunable parameters for the RAG system
# Edit these values to customize behavior

# ============================================
# LLM Configuration
# ============================================
LLM_MODEL = "gpt-4"  # Options: gpt-4, gpt-3.5-turbo
LLM_TEMPERATURE = 0.7  # Range: 0.0-1.0 (0=deterministic, 1=creative)
LLM_MAX_TOKENS = 2048  # Maximum response length

# ============================================
# Embedding Configuration
# ============================================
EMBEDDING_MODEL = "text-embedding-3-small"  # OpenAI embedding model
EMBEDDING_DIMENSION = 1536

# ============================================
# Document Processing
# ============================================
CHUNK_SIZE = 1000  # Size of text chunks for indexing
CHUNK_OVERLAP = 200  # Overlap between chunks for context continuity
SEPARATORS = ["\n\n", "\n", " ", ""]  # Splitting separators in order

# ============================================
# Vector Store & Retrieval
# ============================================
VECTOR_STORE_TYPE = "faiss"  # Type of vector store
VECTOR_STORE_PATH = "faiss_index"  # Path to save/load vector store
TOP_K_RESULTS = 4  # Number of document chunks to retrieve
SIMILARITY_THRESHOLD = 0.5  # Minimum similarity score (0-1)

# ============================================
# Chain Configuration
# ============================================
CHAIN_TYPE = "stuff"  # Options: stuff, map_reduce, refine, map_rerank
CHAIN_VERBOSE = False  # Show detailed chain execution

# ============================================
# Performance Tuning
# ============================================
ENABLE_CACHE = True  # Cache vector store between runs
CACHE_EXPIRY_HOURS = 24  # How long to keep cached index

# ============================================
# UI Configuration
# ============================================
SHOW_SOURCE_DOCS = True  # Show which documents were used
SHOW_SIMILARITY_SCORES = False  # Show retrieval confidence scores
EXAMPLE_QUESTIONS = [
    "What are the guidelines for access arrangements?",
    "How should lecturers support HBL students?",
    "What is the student crisis support procedure?",
    "What languages are considered inclusive and disability-friendly?",
    "What are the misconduct management procedures for students with SEN?"
]

# ============================================
# Cost Optimization
# ============================================
WARN_ON_COST = True  # Warn when significant costs will be incurred
COST_WARNING_THRESHOLD = 0.50  # Cost threshold in USD

# ============================================
# Advanced LLM Parameters
# ============================================
TOP_P = 1.0  # Nucleus sampling (0-1)
FREQUENCY_PENALTY = 0.0  # Penalize repeated tokens (-2 to 2)
PRESENCE_PENALTY = 0.0  # Penalize new tokens (-2 to 2)

# ============================================
# Logging
# ============================================
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "rag_assistant.log"
LOG_QUERIES = True  # Log user queries (ensure privacy compliance)
