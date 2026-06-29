"""Document loading + chunking (Ingestion pipeline → Load / Split boxes)."""
from pathlib import Path
from pypdf import PdfReader
import config


def load_documents():
    """Read every PDF in DATA_DIR into per-page records."""
    docs = []
    for pdf in sorted(Path(config.DATA_DIR).glob("*.pdf")):
        reader = PdfReader(str(pdf))
        for i, page in enumerate(reader.pages):
            text = (page.extract_text() or "").strip()
            if text:
                docs.append({"source": pdf.name, "page": i, "text": text})
    return docs


def split_documents(docs):
    """Fixed-size character chunks with overlap (deterministic)."""
    size, overlap = config.CHUNK_SIZE, config.CHUNK_OVERLAP
    chunks = []
    for d in docs:
        t, start, idx = d["text"], 0, 0
        while start < len(t):
            chunks.append({
                "id": f'{d["source"]}:{d["page"]}:{idx}',
                "text": t[start:start + size],
                "source": d["source"], "page": d["page"],
            })
            start += max(1, size - overlap)
            idx += 1
    return chunks
