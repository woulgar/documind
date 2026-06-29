"""Eval & ops (L0): deterministic box tests, custom KPIs, cost guard."""
import config

try:  # PDM logs KPIs when measured; a no-op stub when run standalone.
    import pdm_log as pdm
except Exception:
    class _Stub:
        def log(self, *a, **k):
            pass
    pdm = _Stub()


def run_box_tests():
    """Deterministic checks for the ingestion boxes."""
    from loader import load_documents, split_documents
    docs = load_documents()
    assert len(docs) >= 2, "expected at least 2 source documents"
    chunks = split_documents(docs)
    assert len(chunks) > 0, "splitter produced no chunks"
    return {"documents": len(docs), "chunks": len(chunks)}


def record_kpis(result):
    """Log answer quality + retrieval hit (box-bound) and a project KPI."""
    docs = result["docs"]
    hit = 1.0 if any("monopoly" in d["source"].lower() for d in docs) else 0.0
    pdm.log("retrieval_hit", hit, unit="0/1", box="retrieve")

    ans = result["answer"].lower()
    quality = 1.0 if any(w in ans for w in ["two", "2", "eight", "8", "player"]) else 0.5
    pdm.log("answer_quality", quality, unit="score", box="llm_answer")

    pdm.log("notes_indexed", len(docs), unit="docs")  # project-level KPI
    return {"retrieval_hit": hit, "answer_quality": quality}


def cost_report():
    """Cost guard placeholder — real per-box tokens come from the PDM trace."""
    return {"budget_usd": config.COST_BUDGET_USD}


def evaluate(result):
    # Box tests and the cost report are independent → run them in parallel
    # (v5: shows up as two boxes lit at once in playback).
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=2) as ex:
        f_tests = ex.submit(run_box_tests)
        f_cost = ex.submit(cost_report)
        f_tests.result()
        f_cost.result()
    kpis = record_kpis(result)
    return kpis
