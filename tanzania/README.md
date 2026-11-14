# Please, You Are So Delusional! (Tanzania)

Flag = the one printed by `python retrieval_pipeline.py` (it is a hash of all 72 answers, so all must be right).

The starter RAG pipeline returned wrong documents. Compared with the organizers' original, we fixed 4 bugs.
(1) Documents and questions were embedded with two different models, so similarity was meaningless. (2) e5 needs
the `passage:` prefix on documents. (3) Documents were cut into 180-character pieces, which lost the title (place
and station).

(4) Old `ARCHIVED` versions of the notices competed with the current ones. After the fixes, each document is one
chunk (title + text), embedded with the same e5 model, and archived documents are skipped.

```python
DOCUMENT_MODEL = "intfloat/e5-small-v2"          # was all-MiniLM-L6-v2 (queries used e5)

if document.title.startswith("ARCHIVED"):        # skip outdated notices
    continue
chunks.append(Chunk(document.document_id, f"{document.title}\n{document.text}"))   # was 180-char slices

[f"passage: {chunk.text}" for chunk in chunks]  # e5 prefix, was missing
```

Run: `pip install -r requirements.txt && python retrieval_pipeline.py`
