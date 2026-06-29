"""Prompt building + answer generation (Generate answer → Build prompt / LLM answer)."""
import re
import ollama
import config


def build_prompt(query, docs):
    """Grounded prompt: only the retrieved context, ask for citations."""
    context = "\n\n---\n\n".join(
        f'[{d["source"]} p.{d["page"]}]\n{d["text"]}' for d in docs)
    return (
        "Answer the question using ONLY the context below. "
        "Cite sources like [file p.N]. If the answer isn't in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {query}\nAnswer: /no_think"
    )


def llm_answer(prompt):
    """Generate the grounded answer with the local answer model (GPU)."""
    resp = ollama.chat(model=config.LLM_MODEL, messages=[{"role": "user", "content": prompt}])
    return re.sub(r"<think>.*?</think>", "", resp["message"]["content"], flags=re.DOTALL).strip()


def generate(query, docs):
    return llm_answer(build_prompt(query, docs))
