"""Retrieval + query rewrite (Query & answer → Retrieve / Rewrite boxes)."""
import re
import config
from embeddings import get_embedding_function
from vectordb import get_collection


_STOP = {"the", "a", "an", "how", "many", "much", "can", "do", "does", "is", "are",
         "of", "to", "in", "on", "for", "what", "which", "who", "and", "or"}


def rewrite_query(query):
    """Extract keywords for retrieval — lexical, no LLM.

    v1-v2 called an LLM here, but PDM measured it burning ~1.6k output tokens per
    run (more than the answer itself) for a one-line query. A stop-word filter does
    the same job for zero tokens. (See benchmark finding.)"""
    words = [w for w in re.findall(r"\w+", query.lower())
             if w not in _STOP and len(w) > 2]
    return " ".join(words) or query


def embed_query(query):
    """Embed the query vector (GPU) — split out of retrieve in v4."""
    return get_embedding_function()([query])[0]


def vector_search(qv, k):
    """Top-k nearest-neighbour lookup in the Chroma store."""
    res = get_collection().query(query_embeddings=[qv], n_results=k)
    docs = []
    for i in range(len(res["ids"][0])):
        meta = res["metadatas"][0][i]
        docs.append({"id": res["ids"][0][i], "text": res["documents"][0][i],
                     "source": meta["source"], "page": meta["page"]})
    return docs


def retrieve(query, k=None):
    """Top-k semantic search = embed the query, then vector-search."""
    return vector_search(embed_query(query), k or config.TOP_K)


def rerank(query, docs):
    """Lexical rerank: reorder retrieved chunks by query-keyword overlap so the
    most on-topic context leads the prompt (cheap, deterministic, no model)."""
    terms = {w for w in re.findall(r"\w+", query.lower()) if len(w) > 2}

    def score(d):
        words = re.findall(r"\w+", d["text"].lower())
        if not words:
            return 0.0
        overlap = sum(1 for w in words if w in terms)
        return overlap / (len(words) ** 0.5)  # length-normalized overlap

    return sorted(docs, key=score, reverse=True)
