"""Local embeddings via Ollama (Ingestion pipeline → Embed box, GPU)."""
import ollama
import config


def get_embedding_function():
    """Returns embed(texts) -> list[vector] using the local embedding model."""
    def embed(texts):
        vectors = []
        for i in range(0, len(texts), 32):
            batch = texts[i:i + 32]
            resp = ollama.embed(model=config.EMBED_MODEL, input=batch)
            vectors.extend(resp["embeddings"])
        return vectors
    return embed


def embed_chunks(chunks):
    """Attach an embedding vector to every chunk (GPU-bound work)."""
    embed = get_embedding_function()
    for chunk, vec in zip(chunks, embed([c["text"] for c in chunks])):
        chunk["embedding"] = vec
    return chunks
