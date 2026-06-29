"""DocuMind configuration — all knobs in one place."""
DATA_DIR = "data"
CHROMA_DIR = "chroma"
COLLECTION = "documind"

# Local Ollama models (nothing leaves the machine).
EMBED_MODEL = "qwen3-embedding:4b"
REWRITE_MODEL = "qwen3:4b"     # cheap model for query rewriting
LLM_MODEL = "qwen3:8b"         # answer model

TOP_K = 5
CHUNK_SIZE = 800
CHUNK_OVERLAP = 80
COST_BUDGET_USD = 0.01         # cost guard threshold per answer

# Deterministic driver input: same docs + same question every run.
FIXED_QUERY = "How many players can play Monopoly?"
