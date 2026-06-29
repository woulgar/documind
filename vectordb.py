"""Local Chroma vector store (Ingestion pipeline → Upsert box)."""
import chromadb
import config

_client = None


def get_collection():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=config.CHROMA_DIR)
    return _client.get_or_create_collection(config.COLLECTION)


def add_to_chroma(chunks):
    """Upsert only chunks not already stored (idempotent ingest)."""
    col = get_collection()
    existing = set(col.get(include=[]).get("ids", []))
    new = [c for c in chunks if c["id"] not in existing]
    if new:
        col.add(
            ids=[c["id"] for c in new],
            embeddings=[c["embedding"] for c in new],
            documents=[c["text"] for c in new],
            metadatas=[{"source": c["source"], "page": c["page"]} for c in new],
        )
    return len(new)
