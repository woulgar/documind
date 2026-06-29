"""Top-level orchestrators (L0 boxes: Ingestion pipeline / Query & answer)."""
from loader import load_documents, split_documents
from embeddings import embed_chunks
from vectordb import add_to_chroma
from retriever import retrieve, rewrite_query, rerank
from generate import generate


def ingest():
    """Load → split → embed → upsert."""
    chunks = embed_chunks(split_documents(load_documents()))
    add_to_chroma(chunks)
    return len(chunks)


def answer(query):
    """Rewrite → retrieve → generate, grounded in the indexed docs."""
    rq = rewrite_query(query)
    docs = retrieve(rq or query)
    docs = rerank(query, docs)
    ans = generate(query, docs)
    return {"query": query, "rewritten": rq, "answer": ans, "docs": docs}
