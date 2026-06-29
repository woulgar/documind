"""PDM deterministic driver for DocuMind.

pdm_flow.py imports this module and calls run() with no args. Same docs +
same fixed question every run, so tokens / time / GPU are comparable across
versions. Authored by the PDM agent from the box map (PDM_SPEC).
"""
from pipeline import ingest, answer
from eval import evaluate
import config


def run():
    ingest()
    result = answer(config.FIXED_QUERY)
    evaluate(result)
    print("Q:", result["query"])
    print("A:", result["answer"][:300])
