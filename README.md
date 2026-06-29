# DocuMind — a local, private PDF Q&A you can measure

DocuMind answers questions about **your own PDFs**, on your machine, with citations.
Nothing leaves the box: the models run on **[Ollama](https://ollama.com)** and the
vectors live in a local **[Chroma](https://www.trychroma.com)** store.

It's also the demo project for **[PDM — Project Density Measures](https://github.com/woulgar/pdm)**:
DocuMind was designed as a box/layer/connector flow map first, then built, and every
version was measured with PDM. The `.pdm/` folder in this repo contains those real
measurements — open it in the PDM viewer to see exactly what each step costs.

> ⚠️ **This is a demo / example project, not a production app.** DocuMind exists to
> *showcase and be measured by PDM* — a small, intentionally simple RAG (no auth, no UI,
> lexical rerank, a single fixed demo question). Don't treat it as a serious, hardened
> RAG library; treat it as a clean, real, end-to-end example you can open in PDM and
> learn from.

## How it works

```
Ingestion pipeline        Query & answer                 Eval & ops
  Load PDFs                  Query rewrite (keywords)       Box tests
  Split into chunks          Retrieve top-k                 Record KPIs
  Embed (GPU)                  Embed query (GPU)            Cost guard
  Upsert to Chroma            Vector search
                            Rerank chunks
                            Generate answer
                              Build prompt
                              LLM answer (GPU)
```

- **Ingestion** (`loader.py` → `embeddings.py` → `vectordb.py`): read every PDF page,
  split into fixed-size overlapping chunks, embed locally, upsert into Chroma
  (idempotent — re-ingesting only adds new chunks).
- **Query & answer** (`retriever.py` → `generate.py`): turn the question into retrieval
  keywords, embed it, vector-search the top-k chunks, rerank by keyword overlap, build a
  grounded prompt and answer with the local model — citing `[file p.N]`.
- **Eval & ops** (`eval.py`): deterministic box tests + custom KPIs (`answer_quality`,
  `retrieval_hit`, `notes_indexed`) + a cost guard.

Everything is deterministic on a fixed question (`config.FIXED_QUERY`) so cost and
timing are comparable across versions.

## Run it

1. Install [Ollama](https://ollama.com) and pull the models (all local, free):
   ```bash
   ollama pull qwen3:8b              # answer model
   ollama pull qwen3:4b              # (legacy) query-rewrite model
   ollama pull qwen3-embedding:4b    # embeddings
   ```
2. Install the Python deps:
   ```bash
   pip install -r requirements.txt
   ```
3. Drop some PDFs into `data/` (see [`data/README.md`](data/README.md)).
4. Ingest + ask the fixed demo question:
   ```bash
   python -c "from pdm_driver import run; run()"
   ```
   Ask your own questions:
   ```bash
   python -c "from pipeline import ingest, answer; ingest(); print(answer('your question?')['answer'])"
   ```

## See what it costs (PDM)

This repo ships its real PDM measurements in `.pdm/` (flow map + per-version traces +
benchmark). Open the folder in the **[PDM viewer](https://github.com/woulgar/pdm)**
(desktop app or VS Code extension → *Open project*) to explore them. Real findings from
these runs:

- **The "cheap" query-rewrite step was the expensive one.** v1–v2 called an LLM to
  rewrite the query; PDM showed it burning more output tokens than the answer itself.
  Replacing it with a stop-word filter (`retriever.rewrite_query`) cut a run from
  **1,661 → 1,192 tokens (−28%)** with the same answer — that step now reads **−100%**.
- **Real local GPU cost, per box.** The answer step peaks at ~**53% GPU / 6.6 GB VRAM**
  on the machine — all measured, all on-device.
- **A 5-agent benchmark** ("add a rerank box"): Codex, Claude and Haiku 4.5 each built
  it; the winner by work-per-token was promoted to the next version.

## License

[MIT](LICENSE) — the code. The board-game rulebooks used in the original measurements
are not included and remain the property of their respective owners.
