"""DocuMind configuration — all knobs in one place."""
import sys
from pathlib import Path

# Owner policy is shared by this local workspace; no independent model defaults.
_POLICY_ROOT = next((p / "company" / "runner" for p in Path(__file__).resolve().parents
                     if (p / "company" / "runner" / "local_ai_policy.py").is_file()), None)
if _POLICY_ROOT is None:
    raise RuntimeError("Company local AI policy is unavailable; refusing inference")
sys.path.insert(0, str(_POLICY_ROOT))
from local_ai_policy import require_model

DATA_DIR = "data"
CHROMA_DIR = "chroma"
COLLECTION = "documind"

# Local Ollama models (nothing leaves the machine).
EMBED_MODEL = "qwen3-embedding:4b"
REWRITE_MODEL = require_model()  # legacy setting; rewrite is deterministic
LLM_MODEL = require_model()      # owner-approved answer model

TOP_K = 5
CHUNK_SIZE = 800
CHUNK_OVERLAP = 80
COST_BUDGET_USD = 0.01         # cost guard threshold per answer

# Deterministic driver input: same docs + same question every run.
FIXED_QUERY = "How many players can play Monopoly?"
